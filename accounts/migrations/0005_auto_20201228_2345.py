# Generated by Django 3.0.11 on 2020-12-28 18:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0004_auto_20201228_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friends',
            name='request_status',
            field=models.CharField(blank=True, choices=[('SENT', 'Request Sent'), ('DONE', 'Accepted Request'), ('BLOCK', 'blocked')], max_length=30),
        ),
        migrations.AlterField(
            model_name='friends',
            name='user_requested',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_requested', to=settings.AUTH_USER_MODEL),
        ),
    ]