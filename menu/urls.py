from django.urls import path

from .views import *
urlpatterns = [

    # Customer menu
    path(
        "",
        menu_list,
        name="menu"
    ),

  
    path(
        "manager/",
        manager_menu,
        name="manager-menu"
    ),

   
    path(
        "manager/category/add/",
        category_create,
        name="category-create"
    ),

    path(
        "manager/category/<int:category_id>/edit/",
        category_edit,
        name="category-edit"
    ),

    path(
        "manager/category/<int:category_id>/delete/",
        category_delete,
        name="category-delete"
    ),

    # Menu items
    path(
        "manager/item/add/",
        menu_item_create,
        name="menu-item-create"
    ),

    path(
        "manager/item/<int:item_id>/edit/",
        menu_item_edit,
        name="menu-item-edit"
    ),

    path(
        "manager/item/<int:item_id>/delete/",
        menu_item_delete,
        name="menu-item-delete"
    ),

]