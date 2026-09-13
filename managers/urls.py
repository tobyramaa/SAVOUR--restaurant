from django.urls import path

from .views import (
    manager_dashboard,
    staff_list,
    staff_detail,
    edit_staff,
    deactivate_staff,
    delete_staff,
)


urlpatterns = [

    path(
        "",
        manager_dashboard,
        name="manager-dashboard"
    ),

    path(
        "staff/",
        staff_list,
        name="manager-staff-list"
    ),

    path(
        "staff/<int:staff_id>/",
        staff_detail,
        name="manager-staff-detail"
    ),

    path(
        "staff/<int:staff_id>/edit/",
        edit_staff,
        name="edit-staff"
    ),

    path(
        "staff/<int:staff_id>/deactivate/",
        deactivate_staff,
        name="deactivate-staff"
    ),

    path(
        "staff/<int:staff_id>/delete/",
        delete_staff,
        name="delete-staff"
    ),

]