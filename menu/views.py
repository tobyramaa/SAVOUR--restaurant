from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Category, MenuItem
from .forms import CategoryForm, MenuItemForm


def menu_list(request):

    categories = Category.objects.all()

    return render(
        request,
        "menu/menu_list.html",
        {"categories": categories}
    )



@login_required
def manager_menu(request):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect("dashboard")

    categories = Category.objects.all()
    menu_items = MenuItem.objects.select_related("category").all()

    return render(
        request,
        "menu/manager_menu.html",
        {
            "categories": categories,
            "menu_items": menu_items,
        }
    )


@login_required
def category_create(request):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect("dashboard")

    if request.method == "POST":

        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("manager-menu")

    else:

        form = CategoryForm()

    return render(
        request,
        "menu/category_form.html",
        {
            "form": form,
            "title": "Add Category",
        }
    )



@login_required
def category_edit(request, category_id):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect("dashboard")

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == "POST":

        form = CategoryForm(
            request.POST,
            instance=category
        )

        if form.is_valid():

            form.save()

            return redirect("manager-menu")

    else:

        form = CategoryForm(
            instance=category
        )

    return render(
        request,
        "menu/category_form.html",
        {
            "form": form,
            "title": "Edit Category",
        }
    )


@login_required
def category_delete(request, category_id):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect("dashboard")

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == "POST":

        category.delete()

        return redirect("manager-menu")

    return render(
        request,
        "menu/category_confirm_delete.html",
        {
            "category": category,
        }
    )



@login_required
def menu_item_create(request):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect("dashboard")

    if request.method == "POST":

        form = MenuItemForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("manager-menu")

    else:

        form = MenuItemForm()

    return render(
        request,
        "menu/menu_item_form.html",
        {
            "form": form,
            "title": "Add Menu Item",
        }
    )



@login_required
def menu_item_edit(request, item_id):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect("dashboard")

    menu_item = get_object_or_404(
        MenuItem,
        id=item_id
    )

    if request.method == "POST":

        form = MenuItemForm(
            request.POST,
            request.FILES,
            instance=menu_item
        )

        if form.is_valid():

            form.save()

            return redirect("manager-menu")

    else:

        form = MenuItemForm(
            instance=menu_item
        )

    return render(
        request,
        "menu/menu_item_form.html",
        {
            "form": form,
            "title": "Edit Menu Item",
        }
    )


@login_required
def menu_item_delete(request, item_id):

    if not request.user.groups.filter(name="Manager").exists():
        return redirect("dashboard")

    menu_item = get_object_or_404(
        MenuItem,
        id=item_id
    )

    if request.method == "POST":

        menu_item.delete()

        return redirect("manager-menu")

    return render(
        request,
        "menu/menu_item_confirm_delete.html",
        {
            "menu_item": menu_item,
        }
    )