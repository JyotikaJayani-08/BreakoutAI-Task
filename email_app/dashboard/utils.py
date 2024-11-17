# dashboard/utils.py
import sendgrid
from sendgrid.helpers.mail import Mail, From, To, Content
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_email(to_address, subject, body):
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    from_email = From(settings.DEFAULT_FROM_EMAIL)  # Use From object
    to_email = To(to_address)  # Use To object

    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        if response.status_code in [200, 202]:
            logger.info(f"Email sent to {to_address}")
            return True
        else:
            logger.error(f"SendGrid error {response.status_code}: {response.body}")
            return False
    except Exception as e:
        logger.error(f"Failed to send email via SendGrid: {e}")
        return False