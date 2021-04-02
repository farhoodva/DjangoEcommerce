from django.urls import path
from.views import HomeView, ProductDetailView, add_remove_to_wishlist
app_name = 'core'

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('', HomeView.as_view(), name='home'),
    path('detail/<slug>', ProductDetailView.as_view(), name='product_detail'),
    path('ajax_wishlist/<slug>', add_remove_to_wishlist, name='add_remove_to_wishlist'),

]