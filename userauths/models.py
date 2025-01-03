
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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


class ActivityLog(models.Model):
    task = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.task} - {self.timestamp}"
    




class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('TECH', 'Tech'),
        ('NEW', 'New'),
        ('INTERESTING', 'Interesting'),
        ('BREAKING', 'Breaking'),
        ('UPDATES', 'Updates'),
        ('NEWS', 'News'),
        ('ARTICLE', 'Article'),
        ('ACHIEVEMENTS', 'Achievements'),
        ('OTHERS', 'Others'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author.username}"