from django.urls import path
from.views import HomeView, ProductDetailView, add_remove_to_wishlist, add_to_cart, CartView
app_name = 'core'

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('', HomeView.as_view(), name='home'),
    path('detail/<slug>', ProductDetailView.as_view(), name='product_detail'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart_view'),
    path('ajax_wishlist/<slug>', add_remove_to_wishlist, name='add_remove_to_wishlist'),

]