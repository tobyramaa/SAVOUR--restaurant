from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm

from .forms import (
    RegistrationForm,
    StaffCreateForm,
    StaffActivationForm
)

from .models import (
    CustomerProfile,
    StaffProfile,
    KitchenProfile,
    RiderProfile
)

import secrets
import resend
import os

from datetime import timedelta
from django.utils import timezone


# Resend API key
resend.api_key = os.environ.get("RESEND_API_KEY")


def home(request):
    return render(
        request,
        "accounts/home.html"
    )


def register(request):

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():

            phone_number = form.cleaned_data.get("phone_number")
            address = form.cleaned_data.get("address")

            user = form.save(commit=False)

            password = form.cleaned_data["password"]

            user.set_password(password)
            user.save()

            CustomerProfile.objects.create(
                user=user,
                phone_number=phone_number,
                address=address
            )

            customer_group = Group.objects.get(
                name="Customer"
            )

            user.groups.add(customer_group)

            login(request, user)

            return redirect("dashboard")

    else:

        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


@login_required
def dashboard(request):

    # Manager
    if request.user.groups.filter(
        name="Manager"
    ).exists():

        return redirect("manager-dashboard")

    # Customer
    is_customer = request.user.groups.filter(
        name="Customer"
    ).exists()

    # Kitchen Staff
    is_kitchen = request.user.groups.filter(
        name="Kitchen Staff"
    ).exists()

    # Waiter
    is_waiter = request.user.groups.filter(
        name="Waiter"
    ).exists()

    # Rider
    is_rider = request.user.groups.filter(
        name="Rider"
    ).exists()

    return render(
        request,
        "accounts/dashboard.html",
        {
            "is_customer": is_customer,
            "is_kitchen": is_kitchen,
            "is_waiter": is_waiter,
            "is_rider": is_rider,
        }
    )


def user_login(request):

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect("dashboard")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form}
    )


def user_logout(request):

    logout(request)

    return redirect("login")


@login_required
def staff_create(request):

    # Only Managers can create staff
    if not request.user.groups.filter(
        name="Manager"
    ).exists():

        return redirect("dashboard")

    if request.method == "POST":

        form = StaffCreateForm(request.POST)

        if form.is_valid():

            phone_number = form.cleaned_data.get("phone_number")
            address = form.cleaned_data.get("address")
            position = form.cleaned_data.get("position")
            role = form.cleaned_data.get("role")
            vehicle_type = form.cleaned_data.get("vehicle_type")
            vehicle_number = form.cleaned_data.get("vehicle_number")

            # Generate activation token
            activation_token = secrets.token_hex(32)

            # Token expires after 24 hours
            activation_expires_at = (
                timezone.now() + timedelta(hours=24)
            )

            # Create staff user
            user = form.save(commit=False)

            user.set_unusable_password()
            user.is_active = False

            user.save()

            # Create StaffProfile
            staff = StaffProfile.objects.create(
                user=user,
                phone_number=phone_number,
                address=address,
                position=position,
                activation_token=activation_token,
                activation_expires_at=activation_expires_at
            )

            # Create KitchenProfile
            if role == "Kitchen Staff":

                KitchenProfile.objects.create(
                    staff=staff
                )

            # Create RiderProfile
            elif role == "Rider":

                RiderProfile.objects.create(
                    staff=staff,
                    vehicle_type=vehicle_type,
                    vehicle_number=vehicle_number
                )

            # Add staff to their group
            group = Group.objects.get(
                name=role
            )

            user.groups.add(group)

            # Create activation link
            activation_link = request.build_absolute_uri(
                f"/accounts/activate/{activation_token}/"
            )

            print("ACTIVATION LINK:")
            print(activation_link)

            # Send activation email using Resend
            resend.Emails.send(
                {
                    "from": "Savouré Restaurant <onboarding@resend.dev>",
                    "to": [user.email],
                    "subject": "Activate Your Staff Account",
                    "html": f"""
                        <h2>Welcome to Savouré Restaurant</h2>

                        <p>Hello {user.first_name},</p>

                        <p>
                            Your staff account has been created.
                        </p>

                        <p>
                            <strong>Username:</strong>
                            {user.username}
                        </p>

                        <p>
                            Please click the link below to activate
                            your account and create your password.
                        </p>

                        <p>
                            <a href="{activation_link}">
                                Activate Your Staff Account
                            </a>
                        </p>

                        <p>
                            This activation link will expire in
                            24 hours.
                        </p>

                        <p>
                            Thank you.
                        </p>
                    """
                }
            )

            return redirect("dashboard")

    else:

        form = StaffCreateForm()

    return render(
        request,
        "accounts/staff_create.html",
        {"form": form}
    )


def activate_staff(request, token):

    try:

        staff = StaffProfile.objects.get(
            activation_token=token
        )

    except StaffProfile.DoesNotExist:

        return render(
            request,
            "accounts/activation_invalid.html"
        )

    # Check if token has expired
    if (
        staff.activation_expires_at
        and timezone.now() > staff.activation_expires_at
    ):

        return render(
            request,
            "accounts/activation_expired.html"
        )

    if request.method == "POST":

        form = StaffActivationForm(request.POST)

        if form.is_valid():

            password = form.cleaned_data.get(
                "password"
            )

            user = staff.user

            # Set the new password
            user.set_password(password)

            # Activate the account
            user.is_active = True

            user.save()

            # Clear activation token
            staff.activation_token = None
            staff.activation_expires_at = None

            staff.save()

            # Send staff to login page
            return redirect("login")

    else:

        form = StaffActivationForm()

    return render(
        request,
        "accounts/activate.html",
        {"form": form}
    )