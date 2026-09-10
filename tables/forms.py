from django import forms
from .models import TableBooking


class TableBookingForm(forms.ModelForm):

    class Meta:
        model = TableBooking
        fields = [
            "booking_date",
            "booking_time",
            "number_of_people",
        ]

        widgets = {
            "booking_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "booking_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
            "number_of_people": forms.NumberInput(
                attrs={"min": 1}
            ),
        }