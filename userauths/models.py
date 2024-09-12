
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
    customer_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    called_received_by = models.CharField(max_length=255, default="None")
    remarks = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)


class Cheque(models.Model):
    handled_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you're linking to the logged-in user
    company_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    cheque_number = models.CharField(max_length=50)
    cheque_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)
    cheque_date = models.DateField()
    mit = models.CharField(max_length=255)  # Adjust as needed for the date format
    reminder_email = models.EmailField()
    extra_reminder_email = models.EmailField(blank=True, null=True)
