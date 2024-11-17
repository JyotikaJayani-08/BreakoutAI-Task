from django.db import models

# Create your models here.
# dashboard/models.py
from django.db import models

class EmailData(models.Model):
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    product = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Pending')  # To track email status

class ScheduledEmail(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    recipient_list = models.TextField()  # Store as comma-separated emails
    batch_size = models.IntegerField(default=10)
    schedule_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class SentScheduledEmail(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    recipient_list = models.TextField()  # Comma-separated emails
    sent_time = models.DateTimeField(auto_now_add=True)
    schedule_time = models.DateTimeField()  # When it was originally scheduled