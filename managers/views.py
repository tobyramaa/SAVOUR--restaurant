from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounts.models import CustomerProfile, StaffProfile
from orders.models import Order
from tables.models import Table


@login_required
def manager_dashboard(request):

    # Only Managers can access this page
    if not request.user.groups.filter(
        name="Manager"
    ).exists():

        return redirect("dashboard")


    total_orders = Order.objects.count()


    pending_orders = Order.objects.filter(
        status="PENDING"
    ).count()


    preparing_orders = Order.objects.filter(
        status="PREPARING"
    ).count()


    ready_orders = Order.objects.filter(
        status="READY"
    ).count()


    completed_orders = Order.objects.filter(
        status="COMPLETED"
    ).count()


    total_customers = CustomerProfile.objects.count()


    total_staff = StaffProfile.objects.count()


    total_tables = Table.objects.count()


    recent_orders = Order.objects.select_related(
        "customer"
    ).order_by(
        "-created_at"
    )[:10]


    return render(
        request,
        "managers/manager_dashboard.html",
        {
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "preparing_orders": preparing_orders,
            "ready_orders": ready_orders,
            "completed_orders": completed_orders,
            "total_customers": total_customers,
            "total_staff": total_staff,
            "total_tables": total_tables,
            "recent_orders": recent_orders,
        }
    )


@login_required
def staff_list(request):

    # Only Managers can access this page
    if not request.user.groups.filter(
        name="Manager"
    ).exists():

        return redirect("dashboard")


    staff_members = StaffProfile.objects.select_related(
        "user"
    ).all().order_by(
        "user__first_name"
    )


    return render(
        request,
        "managers/staff_list.html",
        {
            "staff_members": staff_members,
        }
    )


@login_required
def staff_detail(request, staff_id):

    # Only Managers can access this page
    if not request.user.groups.filter(
        name="Manager"
    ).exists():

        return redirect("dashboard")


    staff = get_object_or_404(
        StaffProfile.objects.select_related("user"),
        id=staff_id
    )


    return render(
        request,
        "managers/staff_detail.html",
        {
            "staff": staff,
        }
    )


@login_required
def deactivate_staff(request, staff_id):

    # Only Managers can access this page
    if not request.user.groups.filter(
        name="Manager"
    ).exists():

        return redirect("dashboard")


    staff = get_object_or_404(
        StaffProfile,
        id=staff_id
    )


    if request.method == "POST":

        staff.user.is_active = False

        staff.user.save()


    return redirect(
        "manager-staff-list"
    )


@login_required
def delete_staff(request, staff_id):

    # Only Managers can access this page
    if not request.user.groups.filter(
        name="Manager"
    ).exists():

        return redirect("dashboard")


    staff = get_object_or_404(
        StaffProfile,
        id=staff_id
    )


    if request.method == "POST":

        staff.user.delete()


    return redirect(
        "manager-staff-list"
    )

