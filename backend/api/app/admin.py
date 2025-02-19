from django.contrib import admin

# Register your models here.

from .models import Product, Category, Order, Address, Cart, Coupon, Delevry, MyUser

admin.site.register(MyUser)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(Coupon)
admin.site.register(Delevry)
