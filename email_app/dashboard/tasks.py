# dashboard/tasks.py
from background_task import background
from .utils import send_email
from .models import EmailData, ScheduledEmail, SentScheduledEmail
import logging
from django.utils import timezone
from datetime import datetime


logger = logging.getLogger(__name__)


@background(schedule=60)  # Sends an email 60 seconds after scheduling
def send_scheduled_email(subject, message, recipient_list):
    """
    Task to send an email to a list of recipients with a specified subject and message.
    """
    for recipient in recipient_list:
        email_sent = send_email(
            to_address=recipient,
            subject=subject,
            body=message
        )
        if email_sent:
            logger.info(f"Email successfully sent to {recipient}")
        else:
            logger.error(f"Failed to send email to {recipient}")


@background(schedule=60)
def schedule_emails(schedule_time_str, batch_size=10):
    logger.info("Started background task for scheduling emails.")

    try:
        schedule_time = datetime.fromisoformat(schedule_time_str)
    except ValueError:
        logger.error(f"Invalid schedule_time format: {schedule_time_str}")
        return

    local_tz = timezone.get_current_timezone()
    schedule_time = schedule_time.astimezone(local_tz)

    scheduled_emails = ScheduledEmail.objects.filter(schedule_time__lte=schedule_time)

    for scheduled_email in scheduled_emails:
        recipient_list = scheduled_email.recipient_list.split(',')
        recipients_to_send = recipient_list[:batch_size]

        for recipient in recipients_to_send:
            email_sent = send_email(
                to_address=recipient,
                subject=scheduled_email.subject,
                body=scheduled_email.message
            )

            if email_sent:
                logger.info(f"Email sent to {recipient} for subject '{scheduled_email.subject}'")
            else:
                logger.error(f"Failed to send email to {recipient} for subject '{scheduled_email.subject}'")

        remaining_recipients = recipient_list[batch_size:]
        if remaining_recipients:
            scheduled_email.recipient_list = ','.join(remaining_recipients)
            scheduled_email.save()
            logger.info(f"Updated scheduled email to include only remaining recipients: {scheduled_email.recipient_list}")
        else:
            try:
                SentScheduledEmail.objects.create(
                    subject=scheduled_email.subject,
                    message=scheduled_email.message,
                    recipient_list=scheduled_email.recipient_list,
                    schedule_time=scheduled_email.schedule_time,
                    sent_time=timezone.now()
                )
                logger.info(f"Transferred email for subject '{scheduled_email.subject}' to SentScheduledEmail.")
                scheduled_email.delete()
                logger.info(f"Deleted scheduled email for subject '{scheduled_email.subject}'")
            except Exception as e:
                logger.error(f"Failed to transfer scheduled email '{scheduled_email.subject}' to SentScheduledEmail: {e}")



@background(schedule=60)
def send_pending_emails(batch_size=10):
    """
    Task to send a batch of pending emails from the EmailData model.
    """
    logger.info("Started background task for sending pending emails.")
    # Get emails with 'Pending' status, up to the specified batch size
    emails = EmailData.objects.filter(status='Pending')[:batch_size]

    for email_data in emails:
        # Construct the email message based on the data
        content = f"Hello {email_data.company_name}, check out our new products in {email_data.location}!"

        # Send the email and update status
        email_sent = send_email(
            to_address=email_data.email,
            subject="Personalized Offer",
            body=content
        )
        email_data.status = 'Sent' if email_sent else 'Failed'
        email_data.save()

        logger.info(f"Email sent to {email_data.email}: {'Success' if email_sent else 'Failed'}")

        if not email_sent:
            logger.error(f"Failed to send email to {email_data.email}")
