from django.contrib import admin

# Register your models here.

from .models import Products, category, Orders, address, Cart, coupon, delevry

admin.site.register(Products)
admin.site.register(category)
admin.site.register(Orders)
admin.site.register(address)
admin.site.register(Cart)
admin.site.register(coupon)
admin.site.register(delevry)
