from django.contrib.auth.models import User
from django.db import models
from datetime import date

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event_name = models.CharField(max_length=200, default='Default Event Name')
    booking_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateField(default=date(2025, 1, 1))  # Use date format instead of string
    number_of_tickets = models.PositiveIntegerField(default=1)  # Provide a default value
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.event_name}"


class Show(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    total_seats = models.IntegerField()
    booked_seats = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Seat(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} for {self.show.name}"
