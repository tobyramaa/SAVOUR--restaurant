from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction

from orders.models import Order


@login_required
def waiter_dashboard(request):

    if not request.user.groups.filter(
        name="Waiter"
    ).exists():
        return redirect("dashboard")

    ready_orders = Order.objects.filter(
        status="READY",
        order_type__in=["DINE_IN", "TAKEAWAY"]
    ).prefetch_related(
        "items__menu_item"
    ).order_by(
        "created_at"
    )

    completed_orders = Order.objects.filter(
        status="COMPLETED",
        order_type__in=["DINE_IN", "TAKEAWAY"]
    ).prefetch_related(
        "items__menu_item"
    ).order_by(
        "-updated_at"
    )

    return render(
        request,
        "waiter/waiter_dashboard.html",
        {
            "ready_orders": ready_orders,
            "completed_orders": completed_orders,
        }
    )


@login_required
def mark_served(request, order_id):

    if not request.user.groups.filter(
        name="Waiter"
    ).exists():
        return redirect("dashboard")

    if request.method == "POST":

        with transaction.atomic():

            order = get_object_or_404(
                Order.objects.select_for_update(),
                id=order_id,
                order_type="DINE_IN"
            )

            if order.status == "READY":
                order.status = "COMPLETED"
                order.save()

    return redirect("waiter-dashboard")


@login_required
def mark_collected(request, order_id):

    if not request.user.groups.filter(
        name="Waiter"
    ).exists():
        return redirect("dashboard")

    if request.method == "POST":

        with transaction.atomic():

            order = get_object_or_404(
                Order.objects.select_for_update(),
                id=order_id,
                order_type="TAKEAWAY"
            )

            if order.status == "READY":
                order.status = "COMPLETED"
                order.save()

    return redirect("waiter-dashboard")