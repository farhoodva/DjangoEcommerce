from django.contrib import admin
from .models import OrderItem, ShoppingCart, Item, Categories, SubCategories

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(ShoppingCart)
admin.site.register(Categories)
admin.site.register(SubCategories)
