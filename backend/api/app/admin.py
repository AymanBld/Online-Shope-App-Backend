from django.contrib import admin

# Register your models here.

from .models import Products, Category, Orders, Address, Cart, Coupon, Delevry, MyUser

admin.site.register(MyUser)
admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Orders)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(Coupon)
admin.site.register(Delevry)
