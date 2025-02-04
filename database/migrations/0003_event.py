# Generated by Django 4.2.11 on 2024-09-08 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_crm_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]
