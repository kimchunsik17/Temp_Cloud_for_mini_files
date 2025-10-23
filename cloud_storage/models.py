from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    password = models.CharField(max_length=4)
    file_id = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True) # Max length for IPv6

    def __str__(self):
        return self.file_id

class GlobalSettings(models.Model):
    max_file_size = models.BigIntegerField(default=50 * 1024 * 1024)  # 50MB default
    max_files_per_ip = models.IntegerField(default=10)

    def __str__(self):
        return "Global Settings"

    def save(self, *args, **kwargs):
        # Ensure there is only one instance of GlobalSettings
        if not self.pk and GlobalSettings.objects.exists():
            raise ValidationError('There can be only one GlobalSettings instance')
        return super(GlobalSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        # Load the single instance of settings, creating it if it doesn't exist
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
