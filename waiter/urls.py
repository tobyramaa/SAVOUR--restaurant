from django.urls import path

from .views import (
    waiter_dashboard,
    mark_served,
    mark_collected,
)


urlpatterns = [

    path(
        "",
        waiter_dashboard,
        name="waiter-dashboard"
    ),

    path(
        "order/<int:order_id>/served/",
        mark_served,
        name="mark-served"
    ),

    path(
        "order/<int:order_id>/collected/",
        mark_collected,
        name="mark-collected"
    ),

]