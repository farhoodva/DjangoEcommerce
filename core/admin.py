from django.contrib import admin
from .models import OrderItem, ShoppingCart, Item, Categories, SubCategories, Coupons, Payment, Reviews
from users.models import UserProfile, State, City
from users.forms import UserProfileEditForm


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'image', 'discount_price', 'warehouse_quantity', 'category', 'slug']
    search_fields = ['title']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['item', 'user', 'positive_exp', 'rating', 'timestamp']
    search_fields = ['title', 'user']


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'ordered_date', 'status']
    search_fields = ['user', 'ordered']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'quantity', 'order_completed']
    search_fields = ['user']


class CouponAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'percentage', 'valid']
    search_fields = ['name', 'amount', 'percentage', 'valid']


class UserProfileAdmin(admin.ModelAdmin):
    form_class = UserProfileEditForm


admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(State)
admin.site.register(Payment)
admin.site.register(City)
admin.site.register(Categories)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Reviews, ReviewAdmin)
admin.site.register(SubCategories,SubCategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Coupons, CouponAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)

