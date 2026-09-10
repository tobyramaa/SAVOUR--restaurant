from django.urls import path
from .views import *

urlpatterns = [
    path("", menu_list, name="menu"),
]