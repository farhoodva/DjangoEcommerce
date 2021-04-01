from django.urls import path
from.views import HomeView, ProductDetailView
app_name = 'core'

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('', HomeView.as_view(), name='home'),
    path('detail/<slug>', ProductDetailView.as_view(), name='product_detail'),

]