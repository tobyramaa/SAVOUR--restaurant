from django.urls import path
from .views import *

urlpatterns = [

    path("",
        home,
        name="home"),
        
    path("register/",
        register, 
        name="register"),

    path("login/",
        user_login,
        name="login"),

    path("logout/",
        user_logout,
        name="logout"),

    path("dashboard/",
        dashboard, 
        name="dashboard"),
        
    path("staff/create/",
        staff_create,
        name="staff-create"),

    path("activate/<str:token>/",
        activate_staff,
        name="activate-staff"),
]