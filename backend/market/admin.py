from django.contrib import admin
from .models import CartItem, Order, Warehouse
# Register your models here.

admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Warehouse)
