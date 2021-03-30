from django.shortcuts import render
from django.views import generic
from .models import Item, Categories


class HomeView(generic.ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'home.html'
    paginate_by = 8

    def get_context_data(self, *args, **kwargs):
        categories= Categories.objects.all()
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories'] = categories
        return context


class ProductDetailView(generic.DetailView):
    model = Item
    template_name = 'detail.html'
