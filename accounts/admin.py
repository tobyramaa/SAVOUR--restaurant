from django.contrib import admin

from .models import (
    StaffProfile,
    CustomerProfile,
    KitchenProfile,
    RiderProfile,
)


admin.site.register(StaffProfile)
admin.site.register(CustomerProfile)
admin.site.register(KitchenProfile)
admin.site.register(RiderProfile)