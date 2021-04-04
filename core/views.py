from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from .models import Item, Categories


class HomeView(generic.ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'home.html'
    paginate_by = 8
    ordering = ['pk']

    def get_context_data(self, *args, **kwargs):
        categories = Categories.objects.all()
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories'] = categories
        return context


class ProductDetailView(generic.DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'detail.html'

    def get_context_data(self, *args, **kwargs):
        item = Item.objects.get(slug=self.kwargs['slug'])
        items = Item.objects.filter(category__pk=item.category.pk).exclude(pk=item.pk)
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['items'] = items
        return context


@login_required
def add_remove_to_wishlist(request, slug):
    item = get_object_or_404(Item, slug=slug)
    if request.user in item.wishlist.all():
        item.wishlist.remove(request.user)
        item.save()
        added_to_wishlist = False
        data = {
            'added_to_wishlist': added_to_wishlist,
       }
        return JsonResponse(data, safe=False)
    else:
        item.wishlist.add(request.user)
        item.save()
        added_to_wishlist = True
        data = {
            'added_to_wishlist': added_to_wishlist,
        }
        return JsonResponse(data, safe=False)\

# @login_required
# def add_remove_to_wishlist2(request, slug):
#     item = get_object_or_404(Item, slug=slug)
#     if request.user in item.wishlist.all():
#         item.wishlist.remove(request.user)
#         item.save()
#         added_to_wishlist = False
#         data = {
#             'added_to_wishlist': added_to_wishlist,
#        }
#         messages.info(request, 'Item removed from wishlist')
#         return HttpResponseRedirect(reverse('core:product_detail', args=[str(slug)]))
#     else:
#         item.wishlist.add(request.user)
#         item.save()
#         added_to_wishlist = True
#         data = {
#             'added_to_wishlist': added_to_wishlist,
#         }
#         messages.info(request, 'Item added to wishlist')
#         return HttpResponseRedirect(reverse('core:product_detail', args=[str(slug)]))