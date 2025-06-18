from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class DrinkItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=True)  # Nullable for existing rows
    name = models.CharField(max_length=100, null=True, blank=True)  # Nullable for existing rows
    email = models.EmailField(null=True, blank=True)  # Nullable for existing rows
    phone = models.CharField(max_length=20, null=True, blank=True)  # Nullable for existing rows
    date = models.DateField()  # Booking date
    time = models.CharField(max_length=5)  # Time like "14:30" to match Flask
    guests = models.PositiveIntegerField()  # Number of guests
    special_requests = models.TextField(blank=True)  # Special requests
    created_at = models.DateTimeField(default=timezone.now)  # Default for existing rows

    def __str__(self):
        return f"{self.name or (self.user.username if self.user else 'Unknown')} - {self.date} {self.time} ({self.guests} guests)"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name