# Generated by Django 4.1.7 on 2023-05-02 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0017_alter_userprofile_email_alter_userprofile_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
    ]
