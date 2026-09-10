from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from orders.models import Order


@login_required
def kitchen_dashboard(request):

    if not request.user.groups.filter(
        name="Kitchen Staff"
    ).exists():
        return redirect("dashboard")

    incoming_orders = Order.objects.filter(
        status__in=["PENDING", "PREPARING"]
    ).prefetch_related(
        "items__menu_item"
    ).order_by(
        "created_at"
    )

    ready_orders = Order.objects.filter(
        status="READY"
    ).prefetch_related(
        "items__menu_item"
    ).order_by(
        "created_at"
    )

    return render(
        request,
        "kitchen/kitchen_dashboard.html",
        {
            "incoming_orders": incoming_orders,
            "ready_orders": ready_orders,
        }
    )

@login_required
def mark_preparing(request, order_id):

    if not request.user.groups.filter(
        name="Kitchen Staff"
    ).exists():
        return redirect("dashboard")

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == "POST":

        if order.status == "PENDING":
            order.status = "PREPARING"
            order.save()

    return redirect("kitchen-dashboard")


@login_required
def mark_ready(request, order_id):

    if not request.user.groups.filter(
        name="Kitchen Staff"
    ).exists():
        return redirect("dashboard")

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == "POST":

        if order.status == "PREPARING":
            order.status = "READY"
            order.save()

    return redirect("kitchen-dashboard")