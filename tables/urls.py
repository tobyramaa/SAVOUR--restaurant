from django.urls import path

from .views import (book_table, booking_success, my_bookings, manager_tables, manager_table_create, manager_table_edit, manager_table_delete,)


urlpatterns = [

    path("book/", book_table, name="book-table"),
    
    path("success/<int:booking_id>/", booking_success, name="booking-success"),

    path("my-bookings/", my_bookings, name="my-bookings"),

    path("manager/tables/", manager_tables, name="manager-tables"),

    path("manager/tables/add/", manager_table_create, name="manager-table-create"),

    path("manager/tables/<int:table_id>/edit/", manager_table_edit, name="manager-table-edit"),

    path("manager/tables/<int:table_id>/delete/", manager_table_delete, name="manager-table-delete"),
]