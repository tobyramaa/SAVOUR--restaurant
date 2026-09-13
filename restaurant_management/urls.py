"""
URL configuration for restaurant_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import home
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path("",home, name="home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('menu/', include('menu.urls')),
    path("orders/", include("orders.urls")),
    path("tables/", include("tables.urls")),
    path("kitchen/", include("kitchen.urls")),
    path("waiter/", include("waiter.urls")),
    path("managers/", include("managers.urls")),
]

urlpatterns += [
    path(
        "media/<path:path>",
        serve,
        {
            "document_root": settings.MEDIA_ROOT,
        },
    ),
]
