# Generated by Django 3.0.11 on 2020-12-24 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_g'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='g',
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='', null=True, upload_to=''),
        ),
    ]