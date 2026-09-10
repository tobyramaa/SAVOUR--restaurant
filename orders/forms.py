from django import forms
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
            self.fields["booking"].queryset = TableBooking.objects.filter(
                customer=user,
                status__in=["PENDING", "CONFIRMED"],
                order__isnull=True
            ).order_by("booking_date", "booking_time")

    def clean(self):
        cleaned_data = super().clean()

        order_type = cleaned_data.get("order_type")
        booking = cleaned_data.get("booking")

        if order_type == "DINE_IN" and not booking:
            self.add_error(
                "booking",
                "Please select a table booking for your dine-in order."
            )

        if order_type == "TAKEAWAY":
            cleaned_data["booking"] = None

        return cleaned_data