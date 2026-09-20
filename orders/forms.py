from datetime import datetime, timedelta

from django import forms
from django.utils import timezone

from tables.models import TableBooking


class CheckoutForm(forms.Form):

    ORDER_TYPE_CHOICES = [
        ("DINE_IN", "Dine-in"),
        ("TAKEAWAY", "Takeaway"),
        # ("DELIVERY", "Delivery"),
    ]

    order_type = forms.ChoiceField(
        choices=ORDER_TYPE_CHOICES,
        widget=forms.RadioSelect
    )

    booking = forms.ModelChoiceField(
        queryset=TableBooking.objects.none(),
        required=False,
        empty_label="Select a table booking",
        widget=forms.Select()
    )

    def __init__(self, *args, **kwargs):

        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if user:

            now = timezone.localtime()

            current_datetime = datetime.combine(
                now.date(),
                now.time().replace(microsecond=0)
            )

            active_bookings = []

            bookings = TableBooking.objects.filter(
                customer=user,
                status="CONFIRMED",
                order__isnull=True
            ).order_by(
                "booking_date",
                "booking_time"
            )

            for booking in bookings:

                # Calculate when the 90-minute booking ends
                booking_start = datetime.combine(
                    booking.booking_date,
                    booking.booking_time
                )

                booking_end = booking_start + timedelta(minutes=90)

                # Only allow bookings whose 90-minute period
                # has not ended
                if booking_end > current_datetime:
                    active_bookings.append(booking)

            self.fields["booking"].queryset = TableBooking.objects.filter(
                id__in=[booking.id for booking in active_bookings]
            ).order_by(
                "booking_date",
                "booking_time"
            )

    def clean(self):

        cleaned_data = super().clean()

        order_type = cleaned_data.get("order_type")
        booking = cleaned_data.get("booking")

        if order_type == "DINE_IN" and not booking:

            self.add_error(
                "booking",
                "Please select a confirmed table booking for your dine-in order."
            )

        if order_type == "TAKEAWAY":

            cleaned_data["booking"] = None

        return cleaned_data