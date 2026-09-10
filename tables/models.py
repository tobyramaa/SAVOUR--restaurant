from django.db import models
from django.contrib.auth.models import User
from orders.models import Order

# Create your models here.

class Table(models.Model):

    TABLE_STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("OCCUPIED", "Occupied"),
        ("RESERVED", "Reserved"),
    ]

    table_number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=TABLE_STATUS_CHOICES, default="AVAILABLE")

    def __str__(self):
        return f"Table {self.table_number}"


class TableBooking(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
        ("COMPLETED", "Completed"),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="table_bookings")
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, related_name="table_booking", null=True, blank=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="bookings", null=True, blank=True)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    number_of_people = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(
            f"{self.customer.username} - Table {self.table.table_number} on {self.booking_date.strftime('%Y-%m-%d')} at {self.booking_time.strftime('%H:%M')}"
        )


