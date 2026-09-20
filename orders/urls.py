from django.urls import path
from .views import *

urlpatterns = [
    path("add/<int:item_id>/", add_to_cart, name="add-to-cart"),
    path("cart/", cart, name="cart"),
    path("checkout/", checkout, name="checkout"),
    path("success/<int:order_id>/", order_success, name="order-success"),
    path("my-orders/", my_orders, name="my-orders"),
    path("manager/orders/", manager_orders, name="manager-orders"),
    path("manager/orders/<int:order_id>/", manager_order_detail, name="manager-order-detail"),
]