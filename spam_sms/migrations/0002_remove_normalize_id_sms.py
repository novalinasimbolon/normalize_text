# Generated by Django 3.0.7 on 2021-03-26 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spam_sms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='normalize',
            name='id_sms',
        ),
    ]
