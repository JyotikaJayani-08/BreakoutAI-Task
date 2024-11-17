# dashboard/management/commands/clear_scheduled_emails.py
from django.core.management.base import BaseCommand
from dashboard.models import ScheduledEmail

class Command(BaseCommand):
    help = 'Clears all scheduled emails'

    def handle(self, *args, **kwargs):
        count, _ = ScheduledEmail.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} scheduled emails'))