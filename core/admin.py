from django.contrib import admin
from .models import OrderItem, ShoppingCart, Item, Categories, SubCategories
from users.models import UserProfile


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'image', 'discount_price', 'warehouse_quantity', 'category', 'slug']
    search_fields = ['title']


admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(ShoppingCart)
admin.site.register(Categories)
admin.site.register(SubCategories,SubCategoryAdmin)
admin.site.register(UserProfile)
