from django.contrib import admin
from .models import Table, TableBooking


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("table_number", "capacity", "status")


@admin.register(TableBooking)
class TableBookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "order",
        "table",
        "booking_date",
        "booking_time",
        "number_of_people",
        "status",
    )