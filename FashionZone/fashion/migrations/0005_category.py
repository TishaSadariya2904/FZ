# Generated by Django 4.1.7 on 2023-04-09 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0004_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
