from django.db import models

# Create your models here.
class normalize(models.Model):
    nama_responden = models.CharField(max_length=50)
    sms_spam = models.CharField(max_length=255)