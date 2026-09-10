from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    activation_token = models.CharField(max_length=255, blank=True, null=True)
    activation_expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Customer"

class KitchenProfile(models.Model):
    staff = models.OneToOneField(StaffProfile, on_delete=models.CASCADE, related_name='kitchen_profile')


    def __str__(self):
        return f"{self.staff.user.get_full_name()} - {self.staff.position}"

class RiderProfile(models.Model):
    staff = models.OneToOneField(StaffProfile, on_delete=models.CASCADE, related_name='rider_profile')
    vehicle_type = models.CharField(max_length=50, blank=True, null=True)
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.staff.user.get_full_name()} - Rider"