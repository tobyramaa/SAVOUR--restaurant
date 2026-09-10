from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

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

            suitable_tables = Table.objects.filter(
                status="AVAILABLE",
                capacity__gte=number_of_people
            ).order_by("capacity")

            available_table = None

            for table in suitable_tables:

                already_booked = TableBooking.objects.filter(
                    table=table,
                    booking_date=booking_date,
                    booking_time=booking_time,
                    status__in=["PENDING", "CONFIRMED"]
                ).exists()

                if not already_booked:
                    available_table = table
                    break

            if not available_table:

                form.add_error(
                    None,
                    "Sorry, there is no suitable table available for this date and time."
                )

            else:

                booking = form.save(commit=False)

                booking.customer = request.user
                booking.table = available_table
                booking.status = "PENDING"

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

    bookings = TableBooking.objects.filter(
        customer=request.user
    ).order_by(
        "-booking_date",
        "-booking_time"
    )

    return render(
        request,
        "tables/my_bookings.html",
        {
            "bookings": bookings
        }
    )