# Generated by Django 5.0.6 on 2024-09-11 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0002_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
