# dashboard/views.py
import csv
from datetime import datetime, timedelta
import pandas as pd
from pytz import timezone as pytz_timezone
from django.utils import timezone
from background_task import background
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from google.oauth2 import credentials as google_credentials
from .google_sheets import get_google_flow, get_google_sheets_data
from .models import EmailData, ScheduledEmail, SentScheduledEmail
from .utils import send_email
from .tasks import schedule_emails
import logging
from django.core.mail import send_mail
logger = logging.getLogger(__name__)


# Home page view
def home(request):
    return render(request, 'dashboard/index.html')


# Handle file uploads (CSV, XLSX) with dynamic column detection
def upload_file(request):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        file_extension = uploaded_file.name.split('.')[-1].lower()

        try:
            if file_extension == 'csv':
                data = pd.read_csv(uploaded_file)
            elif file_extension in ['xls', 'xlsx']:
                data = pd.read_excel(uploaded_file)
            else:
                messages.error(request, "Unsupported file format. Please upload a CSV or Excel file.")
                return redirect('upload_file')

            columns = data.columns.tolist()

            # Validate required columns
            required_columns = ['Company Name', 'Location', 'Email', 'Product']
            if not all(col in columns for col in required_columns):
                missing = list(set(required_columns) - set(columns))
                messages.error(request, f"Missing required columns: {', '.join(missing)}")
                return redirect('upload_file')

            for _, row in data.iterrows():
                EmailData.objects.create(
                    company_name=row.get('Company Name', 'Default Company'),
                    location=row.get('Location', 'Unknown Location'),
                    email=row.get('Email', 'no-email@example.com'),
                    product=row.get('Product', 'N/A')
                )

            messages.success(request, "File uploaded and data processed successfully!")
            return render(request, 'dashboard/upload_success.html', {'columns': columns})

        except Exception as e:
            logger.error(f"Error processing uploaded file: {e}")
            messages.error(request, f"An error occurred while processing the file: {e}")
            return redirect('upload_file')

    return render(request, 'dashboard/upload_file.html')


# Google Sheets authorization flow
def authorize_google_sheets(request):
    flow = get_google_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['state'] = state
    return redirect(authorization_url)


# Google Sheets callback handler
def oauth2callback(request):
    flow = get_google_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    messages.success(request, "Google Sheets authorization successful!")
    return redirect('fetch_google_sheet')


# Fetch data from Google Sheets and save to the database
def fetch_google_sheet(request):
    spreadsheet_id = settings.SPREADSHEET_ID
    range_name = 'Sheet1!A:D'

    credentials_data = request.session.get('credentials')
    if not credentials_data:
        return redirect('authorize_google_sheets')

    credentials = google_credentials.Credentials(**credentials_data)
    try:
        values = get_google_sheets_data(credentials, spreadsheet_id, range_name)

        # Validate data
        if not values or len(values) < 2:
            messages.error(request, "No data found in the Google Sheet.")
            return redirect('home')

        for row in values[1:]:
            if len(row) < 4:
                logger.warning(f"Incomplete row data: {row}")
                continue
            EmailData.objects.create(
                company_name=row[0],
                location=row[1],
                email=row[2],
                product=row[3]
            )

        messages.success(request, "Data fetched from Google Sheets successfully!")
        return render(request, 'dashboard/fetch_success.html', {"data": values})

    except Exception as e:
        logger.error(f"Error fetching data from Google Sheets: {e}")
        messages.error(request, f"An error occurred while fetching data: {e}")
        return redirect('home')


# Customizable email prompt with placeholders
def send_custom_emails(request):
    if request.method == 'POST':
        template = request.POST.get('email_template')

        # Ensure template is provided
        if not template:
            messages.error(request, "Email template cannot be empty.")
            return redirect('send_custom_emails')

        try:
            for email_data in EmailData.objects.filter(status='Pending'):
                email_content = process_template(template, email_data)
                email_sent = send_email(
                    to_address=email_data.email,
                    subject="Personalized Offer",
                    body=email_content
                )
                email_data.status = 'Sent' if email_sent else 'Failed'
                email_data.save()

                if not email_sent:
                    logger.error(f"Failed to send email to {email_data.email}")

            messages.success(request, "Emails sent successfully!")
        except Exception as e:
            logger.error(f"Error sending custom emails: {e}")
            messages.error(request, "An error occurred while sending emails.")

        return redirect('home')

    # Fetch distinct column names for placeholders
    column_names = ['company_name', 'location', 'email', 'product']

    return render(request, 'dashboard/send_custom_emails.html', {'columns': column_names})

def sent_scheduled_emails_view(request):
    sent_emails = SentScheduledEmail.objects.all().order_by('-sent_time')
    return render(request, 'dashboard/sent_scheduled_emails.html', {'sent_emails': sent_emails})
# Utility to process placeholders in email content
def process_template(template, data):
    return template.format(
        company_name=data.company_name,
        location=data.location,
        email=data.email,
        product=data.product
    )


# Trigger email scheduling (to start the background task)
def trigger_email_scheduling(request):
    if request.method == 'POST':
        logger.info("POST request received for scheduling emails.")
        try:
            # Set the schedule time to 60 seconds from now
            schedule_time = datetime.now() + timedelta(seconds=60)
            schedule_emails(schedule_time=schedule_time)  # Pass the schedule_time argument
            messages.success(request, "Email scheduling triggered!")
        except Exception as e:
            logger.error(f"Error scheduling emails: {e}")
            messages.error(request, "Failed to schedule emails.")
        return redirect('schedule_email_view')  # Redirect to the schedule email view
    else:
        return HttpResponse("Method Not Allowed", status=405)



# Background task to send a batch of emails
# @background(schedule=60)
# def schedule_emails(batch_size=10):
#     logger.info("Started background task for scheduling emails.")
#     emails = EmailData.objects.filter(status='Pending')[:batch_size]
#     for email_data in emails:
#         content = f"Hello {email_data.company_name}, check out our new products in {email_data.location}!"
#         email_sent = send_email(
#             to_address=email_data.email,
#             subject="Personalized Offer",
#             body=content
#         )
#         email_data.status = 'Sent' if email_sent else 'Failed'
#         email_data.save()
#         logger.info(f"Email sent to {email_data.email}: {'Success' if email_sent else 'Failed'}")
#
#
#         if not email_sent:
#             logger.error(f"Failed to send email to {email_data.email}")
# Schedule email view
def schedule_email_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient_list = request.POST.get('recipient_list')
        batch_size = int(request.POST.get('batch_size', 10))
        schedule_time = request.POST.get('schedule_time')

        if recipient_list:
            recipient_list = recipient_list.split(',')
        else:
            messages.error(request, "Recipient list cannot be empty.")
            return redirect('schedule_email_view')

        try:
            schedule_time_obj = datetime.strptime(schedule_time, '%Y-%m-%dT%H:%M')
            gmt_plus_530 = pytz_timezone('Asia/Kolkata')
            schedule_time_obj = gmt_plus_530.localize(schedule_time_obj)
        except Exception as e:
            logger.error(f"Error parsing schedule time: {e}")
            messages.error(request, "Invalid schedule time format.")
            return redirect('schedule_email_view')

        ScheduledEmail.objects.create(
            subject=subject,
            message=message,
            recipient_list=','.join(recipient_list),
            batch_size=batch_size,
            schedule_time=schedule_time_obj
        )

        schedule_time_str = schedule_time_obj.isoformat()
        schedule_emails(schedule_time_str=schedule_time_str, batch_size=batch_size)

        messages.success(request, "Email scheduled successfully!")
        return redirect('schedule_email_view')

    scheduled_emails = ScheduledEmail.objects.all()
    for email in scheduled_emails:
        email.schedule_time = email.schedule_time.astimezone(pytz_timezone('Asia/Kolkata'))
    return render(request, 'dashboard/schedule_email.html', {'scheduled_emails': scheduled_emails})


def send_email_via_sendgrid(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )


def test_email(request):
    try:
        send_mail(
            'Test Email',
            'This is a test email.',
            settings.DEFAULT_FROM_EMAIL,
            ['22052982@kiit.ac.in'],
            fail_silently=False,
        )
        return HttpResponse("Email sent successfully!")
    except Exception as e:
        return HttpResponse(f"Error sending email: {e}")