from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    city_address = models.CharField(max_length=100, default='Unknown')

    def __str__(self):
        return self.user.username

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
]
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(default=datetime.time(9, 0))  # Default time set to 9:00 AM
    doctor = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Appointment with {self.doctor} on {self.date} at {self.time}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    city_address = models.CharField(max_length=100, default='Unknown')

    def __str__(self):
        return self.user.username

class PromotionalOffer(models.Model):
    image = models.ImageField(upload_to='promotional_offers/')
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title if self.title else "Promotional Offer"

class Profit(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_logged = models.DateTimeField(default=timezone.now)