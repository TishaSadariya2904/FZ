# Generated by Django 4.1.7 on 2023-05-02 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0015_userprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='password',
            field=models.TextField(null=True),
        ),
    ]