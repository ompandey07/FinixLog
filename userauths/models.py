from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class customuser(AbstractUser):
    is_employee = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    age = models.IntegerField()
    profile_image = models.ImageField(upload_to='employee_profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"