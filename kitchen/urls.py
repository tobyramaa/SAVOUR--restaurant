from django.urls import path

from .views import (
    kitchen_dashboard,
    mark_preparing,
    mark_ready,
)


urlpatterns = [

    path(
        "",
        kitchen_dashboard,
        name="kitchen-dashboard"
    ),

    path(
        "order/<int:order_id>/preparing/",
        mark_preparing,
        name="mark-preparing"
    ),

    path(
        "order/<int:order_id>/ready/",
        mark_ready,
        name="mark-ready"
    ),

]