from django.shortcuts import render
from .models import Category

# Create your views here.

def menu_list(request):

    categories = Category.objects.all()

    return render(
        request,
        "menu/menu_list.html",
        {"categories": categories}
    )