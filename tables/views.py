from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import TableBookingForm
from .models import TableBooking, Table


@login_required
def book_table(request):

    if request.method == "POST":

        form = TableBookingForm(request.POST)

        if form.is_valid():

            booking_date = form.cleaned_data["booking_date"]
            booking_time = form.cleaned_data["booking_time"]
            number_of_people = form.cleaned_data["number_of_people"]

            # Combine the selected date and time
            requested_start = datetime.combine(
                booking_date,
                booking_time
            )

            # Get the current date and time
            now = timezone.localtime()

            current_datetime = datetime.combine(
                now.date(),
                now.time().replace(microsecond=0)
            )

            # Prevent bookings for a time that has already passed
            if requested_start <= current_datetime:

                form.add_error(
                    None,
                    "You cannot book a table for a date or time that has already passed."
                )

            else:

                # Each table booking lasts for 90 minutes
                requested_end = requested_start + timedelta(minutes=90)

                # Find tables that can accommodate the number of people
                suitable_tables = Table.objects.filter(
                    status="AVAILABLE",
                    capacity__gte=number_of_people
                ).order_by("capacity")

                available_table = None

                for table in suitable_tables:

                    # Get bookings for this table on the selected date
                    existing_bookings = TableBooking.objects.filter(
                        table=table,
                        booking_date=booking_date,
                        status__in=["PENDING", "CONFIRMED"]
                    )

                    table_is_available = True

                    for existing_booking in existing_bookings:

                        existing_start = datetime.combine(
                            existing_booking.booking_date,
                            existing_booking.booking_time
                        )

                        existing_end = existing_start + timedelta(minutes=90)

                        # Check whether the two 90-minute periods overlap
                        if (
                            existing_start < requested_end
                            and existing_end > requested_start
                        ):
                            table_is_available = False
                            break

                    if table_is_available:

                        available_table = table
                        break

                if not available_table:

                    form.add_error(
                        None,
                        "Sorry, there is no suitable table available for "
                        "this date and time. Please choose another time."
                    )

                else:

                    booking = form.save(commit=False)

                    # Assign the booking to the logged-in customer
                    booking.customer = request.user

                    # Assign the available table
                    booking.table = available_table

                    # Automatically confirm the booking
                    booking.status = "CONFIRMED"

                    booking.save()

                    return redirect(
                        "booking-success",
                        booking_id=booking.id
                    )

    else:

        form = TableBookingForm()

    return render(
        request,
        "tables/book_table.html",
        {
            "form": form
        }
    )


@login_required
def booking_success(request, booking_id):

    booking = get_object_or_404(
        TableBooking,
        id=booking_id,
        customer=request.user
    )

    return render(
        request,
        "tables/booking_success.html",
        {
            "booking": booking
        }
    )


@login_required
def my_bookings(request):

    # Get the current date and time
    now = timezone.localtime()

    current_datetime = datetime.combine(
        now.date(),
        now.time().replace(microsecond=0)
    )

    active_bookings = []

    bookings = TableBooking.objects.filter(
        customer=request.user
    ).order_by(
        "-booking_date",
        "-booking_time"
    )

    for booking in bookings:

        # Calculate when the 90-minute booking ends
        booking_start = datetime.combine(
            booking.booking_date,
            booking.booking_time
        )

        booking_end = booking_start + timedelta(minutes=90)

        # Only show bookings whose 90-minute period has not ended
        if booking_end > current_datetime:
            active_bookings.append(booking)

    return render(
        request,
        "tables/my_bookings.html",
        {
            "bookings": active_bookings
        }
    )


# ==========================================================
# MANAGER TABLE MANAGEMENT
# ==========================================================

@login_required
def manager_tables(request):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect("dashboard")

    tables = Table.objects.all().order_by("table_number")

    return render(
        request,
        "tables/manager_tables.html",
        {
            "tables": tables
        }
    )


@login_required
def manager_table_create(request):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect("dashboard")

    if request.method == "POST":

        table_number = request.POST.get("table_number")
        capacity = request.POST.get("capacity")

        if table_number and capacity:

            Table.objects.create(
                table_number=table_number,
                capacity=capacity,
                status="AVAILABLE"
            )

            return redirect("manager-tables")

    return render(
        request,
        "tables/manager_table_form.html",
        {
            "title": "Add Table"
        }
    )


@login_required
def manager_table_edit(request, table_id):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect("dashboard")

    table = get_object_or_404(
        Table,
        id=table_id
    )

    if request.method == "POST":

        table_number = request.POST.get("table_number")
        capacity = request.POST.get("capacity")
        status = request.POST.get("status")

        if table_number and capacity and status:

            table.table_number = table_number
            table.capacity = capacity
            table.status = status

            table.save()

            return redirect("manager-tables")

    return render(
        request,
        "tables/manager_table_form.html",
        {
            "title": "Edit Table",
            "table": table
        }
    )


@login_required
def manager_table_delete(request, table_id):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect("dashboard")

    table = get_object_or_404(
        Table,
        id=table_id
    )

    if request.method == "POST":

        table.delete()

        return redirect("manager-tables")

    return render(
        request,
        "tables/manager_table_confirm_delete.html",
        {
            "table": table
        }
    )