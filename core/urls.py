from django.urls import path
from.views import HomeView, ProductDetailView, add_remove_to_wishlist, add_to_cart,\
    remove_from_cart , CartView, remove_order_item, add_coupon, remove_coupon
app_name = 'core'

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('', HomeView.as_view(), name='home'),
    path('detail/<slug>', ProductDetailView.as_view(), name='product_detail'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>', remove_from_cart, name='remove_from_cart'),
    path('remove_order_item/<slug>', remove_order_item, name='remove_order_item'),
    path('add_coupon/', add_coupon, name='add_coupon'),
    path('remove_coupon/', remove_coupon, name='remove_coupon'),
    path('cart/', CartView.as_view(), name='cart_view'),
    path('ajax_wishlist/<slug>', add_remove_to_wishlist, name='add_remove_to_wishlist'),

]