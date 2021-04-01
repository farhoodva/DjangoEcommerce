from django.contrib import admin
from .models import OrderItem, ShoppingCart, Item, Categories, SubCategories
from users.models import UserProfile

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(ShoppingCart)
admin.site.register(Categories)
admin.site.register(SubCategories)
admin.site.register(UserProfile)
