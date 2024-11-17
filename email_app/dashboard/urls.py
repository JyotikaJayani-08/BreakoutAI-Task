# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('schedule_emails/', views.trigger_email_scheduling, name='schedule_emails'),
    path('authorize_google_sheets/', views.authorize_google_sheets, name='authorize_google_sheets'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('fetch_google_sheet/', views.fetch_google_sheet, name='fetch_google_sheet'),
    path('send_custom_emails/', views.send_custom_emails, name='send_custom_emails'),
    path('test_email/', views.test_email, name='test_email'),
    path('schedule_email_view/', views.schedule_email_view, name='schedule_email_view'),
    path('sent-scheduled-emails/', views.sent_scheduled_emails_view, name='sent_scheduled_emails'),
]