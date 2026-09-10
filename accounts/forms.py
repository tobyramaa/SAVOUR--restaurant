from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    phone_number = forms.CharField(
        required=False
    )

    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "rows": 3
        })
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "address",
            "password",
        ]


class StaffCreateForm(forms.ModelForm):

    ROLE_CHOICES = [
        ("Waiter", "Waiter"),
        ("Kitchen Staff", "Kitchen Staff"),
        ("Rider", "Rider"),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES
    )

    phone_number = forms.CharField(
        required=False
    )

    address = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    position = forms.CharField(
        required=False
    )

    vehicle_type = forms.CharField(
        required=False
    )

    vehicle_number = forms.CharField(
        required=False
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "phone_number",
            "address",
            "position",
            "vehicle_type",
            "vehicle_number",
        ]


class StaffActivationForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
