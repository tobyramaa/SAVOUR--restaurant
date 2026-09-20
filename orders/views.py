from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from menu.models import MenuItem
from .models import Order, OrderItem
from .forms import CheckoutForm
from tables.models import TableBooking, Table
from datetime import datetime, timedelta
# Create your views here.

@login_required
def add_to_cart(request, item_id):

    item = get_object_or_404(
        MenuItem,
        id=item_id,
        is_available=True
    )

    cart = request.session.get("cart", {})

    item_id = str(item_id)

    if item_id in cart:
        cart[item_id] += 1
    else:
        cart[item_id] = 1

    request.session["cart"] = cart

    return redirect("menu")


@login_required
def cart(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total_price = 0

    for item_id, quantity in cart.items():
        item = get_object_or_404(MenuItem, id=item_id)
        subtotal = item.price * quantity
        total_price += subtotal
        cart_items.append({"item": item, "quantity": quantity, "subtotal": subtotal})

    return render(request, "orders/cart.html", {"cart_items": cart_items, "total_price": total_price})

@login_required
def checkout(request):

    cart = request.session.get("cart", {})

    if not cart:
        return redirect("cart")

    cart_items = []
    total_price = 0

    for item_id, quantity in cart.items():

        item = get_object_or_404(
            MenuItem,
            id=item_id,
            is_available=True
        )

        subtotal = item.price * quantity
        total_price += subtotal

        cart_items.append({
            "item": item,
            "quantity": quantity,
            "subtotal": subtotal
        })

    if request.method == "POST":

        form = CheckoutForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            order_type = form.cleaned_data["order_type"]
            booking = form.cleaned_data.get("booking")

            # CREATE ORDER
            order = Order.objects.create(
                customer=request.user,
                order_type=order_type,
                total_price=total_price
            )

            # CONNECT ORDER TO EXISTING TABLE BOOKING
            if order_type == "DINE_IN":

                booking.order = order
                booking.save()

            # CREATE ORDER ITEMS
            for cart_item in cart_items:

                OrderItem.objects.create(
                    order=order,
                    menu_item=cart_item["item"],
                    quantity=cart_item["quantity"],
                    price=cart_item["item"].price
                )

            # CLEAR CART
            request.session["cart"] = {}

            return redirect(
                "order-success",
                order_id=order.id
            )

    else:

        form = CheckoutForm(
            user=request.user
        )

    return render(
        request,
        "orders/checkout.html",
        {
            "form": form,
            "cart_items": cart_items,
            "total_price": total_price
        }
    )

@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    booking = getattr(order, "table_booking", None)

    return render(
        request,
        "orders/order_success.html",
        {
            "order": order,
            "booking": booking,
        }
    )


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        customer=request.user
    ).order_by("-created_at")

    return render(
        request,
        "orders/my_orders.html",
        {"orders": orders}
    )

@login_required
def manager_orders(request):

    if not request.user.groups.filter(
        name="Manager"
    ).exists():
        return redirect("dashboard")

    orders = Order.objects.select_related(
        "customer"
    ).prefetch_related(
        "items__menu_item"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "orders/manager_orders.html",
        {
            "orders": orders,
        }
    )



@login_required
def manager_order_detail(request, order_id):

    if not request.user.groups.filter(
        name="Manager"
    ).exists():
        return redirect("dashboard")

    order = get_object_or_404(
        Order.objects.select_related(
            "customer"
        ).prefetch_related(
            "items__menu_item"
        ),
        id=order_id
    )

    order_items = []

    for item in order.items.all():

        subtotal = item.price * item.quantity

        order_items.append({
            "item": item,
            "subtotal": subtotal,
        })

    return render(
        request,
        "orders/manager_order_detail.html",
        {
            "order": order,
            "order_items": order_items,
        }
    )