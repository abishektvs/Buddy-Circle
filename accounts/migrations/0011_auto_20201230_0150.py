# Generated by Django 3.0.11 on 2020-12-29 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20201230_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='', null=True, upload_to=''),
        ),
    ]
