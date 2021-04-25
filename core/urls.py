from django.urls import path
from.views import HomeView, ProductDetailView, add_remove_to_wishlist, add_to_cart,\
    remove_from_cart, CartView, remove_order_item, add_coupon, remove_coupon, search, \
    ajax_load_products, UserBillingView, add_to_cart_multiple, ShopView, SubCatView, CatView
app_name = 'core'

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('', HomeView.as_view(), name='home'),
    path('detail/<slug>', ProductDetailView.as_view(), name='product_detail'),
    path('add_to_cart_multiple/<slug>',add_to_cart_multiple, name='add_to_cart_multiple'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>', remove_from_cart, name='remove_from_cart'),
    path('remove_order_item/<slug>', remove_order_item, name='remove_order_item'),
    path('add_coupon/', add_coupon, name='add_coupon'),
    path('remove_coupon/', remove_coupon, name='remove_coupon'),
    path('Cart/', CartView.as_view(), name='cart_view'),
    path('SubCatView/<int:pk>', SubCatView.as_view(), name='sub_cat_view'),
    path('CatView/<int:pk>', CatView.as_view(), name='cat_view'),
    path('Shop/', ShopView.as_view(), name='shop_view'),
    path('checkout/<int:pk>', UserBillingView.as_view(), name='checkout'),
    path('ajax_wishlist/<slug>', add_remove_to_wishlist, name='add_remove_to_wishlist'),
    path('ajax_load_products/<int:display>', ajax_load_products, name='ajax_load_products'),
    path('search', search, name='search'),

]