from django.urls import path
from .views import book_table, booking_success, my_bookings


urlpatterns = [
    path("book/", book_table, name="book-table"),
    path("success/<int:booking_id>/", booking_success, name="booking-success"),
    path("my-bookings/", my_bookings, name="my-bookings"),
]