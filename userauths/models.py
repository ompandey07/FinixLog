
from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    contact = models.CharField(max_length=15)
    age = models.PositiveIntegerField()
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)


class Inquiry(models.Model):
    date = models.DateField()
    miti = models.CharField(blank=True, null=True, max_length=255)
    customer_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    called_received_by = models.CharField(max_length=255, default="None")
    remarks = models.TextField(blank=True, null=True)
    STATUS_CHOICES = [
        ('new', 'New'),
        ('on_progress', 'On Progress'),
        ('reverted', 'Reverted'),
        ('confirmed', 'Confirmed'),
        ('sold', 'Sold'),
        ('not_fixed', 'Not Fixed'),
        ('declined', 'Declined'),
        ('mood_changed', 'Mood Changed'),
        ('others', 'Others'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')  # Changed field



class Cheque(models.Model):
    handled_by = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    cheque_number = models.CharField(max_length=50)
    cheque_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)
    cheque_date = models.DateField()
    cheque_miti = models.CharField(max_length=255) 
    reminder_email = models.EmailField()
    extra_reminder_email = models.EmailField(blank=True, null=True)
    diposited = models.BooleanField(default=False)
    pending_status = models.BooleanField(default=True)
