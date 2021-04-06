from django.contrib import admin
from .models import OrderItem, ShoppingCart, Item, Categories, SubCategories, Coupons
from users.models import UserProfile


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'image', 'discount_price', 'warehouse_quantity', 'category', 'slug']
    search_fields = ['title']


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']
    search_fields = ['user', 'ordered']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'quantity']
    search_fields = ['user']


class CouponAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'percentage', 'valid']
    search_fields = ['name', 'amount', 'percentage', 'valid']

admin.site.register(UserProfile)
admin.site.register(Categories)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(SubCategories,SubCategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Coupons, CouponAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)

