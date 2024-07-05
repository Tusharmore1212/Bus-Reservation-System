from django.db import models
from django.contrib.auth.models import User
class Bus(models.Model):
    bus_name = models.CharField(max_length=255)
    seat_price = models.DecimalField(max_digits=6, decimal_places=2)
    bus_no = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    date = models.DateField()
    seat = models.PositiveIntegerField(default=1)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    num_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    reservation_date = models.DateTimeField(auto_now_add=True)

