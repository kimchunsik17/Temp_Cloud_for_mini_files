from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from cloud_storage.models import UploadedFile, GlobalSettings
import os

class Command(BaseCommand):
    help = 'Deletes files that are older than the configured auto-delete period.'

    def handle(self, *args, **options):
        settings = GlobalSettings.load()
        auto_delete_days = settings.auto_delete_days

        if auto_delete_days > 0:
            self.stdout.write(f'Auto-delete is enabled for files older than {auto_delete_days} days.')
            cutoff_date = timezone.now() - timedelta(days=auto_delete_days)
            old_files = UploadedFile.objects.filter(created_at__lt=cutoff_date)
            
            count = old_files.count()
            if count > 0:
                self.stdout.write(f'Found {count} old files to delete.')
                for old_file in old_files:
                    # Delete file from filesystem
                    if os.path.exists(old_file.file.path):
                        try:
                            os.remove(old_file.file.path)
                            self.stdout.write(self.style.SUCCESS(f'Successfully deleted file: {old_file.file.path}'))
                        except OSError as e:
                            self.stdout.write(self.style.ERROR(f'Error deleting file {old_file.file.path}: {e}'))
                    
                    # Delete from database
                    old_file.delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} old files.'))
            else:
                self.stdout.write('No old files to delete.')
        else:
            self.stdout.write('Auto-delete is disabled.')
