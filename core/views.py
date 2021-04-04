from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from .models import Item, Categories, OrderItem, ShoppingCart


class HomeView(generic.ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'home.html'
    paginate_by = 8
    ordering = 'pk'

    def get_context_data(self, *args, **kwargs):
        categories = Categories.objects.all()
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories'] = categories
        return context


class CartView(LoginRequiredMixin, generic.ListView):
    # model = ShoppingCart
    context_object_name = 'cart'
    template_name = 'cart.html'

    def get_queryset(self):

        qs = ShoppingCart.objects.get(user_id=self.request.user.id, ordered=False)
        return qs


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



@login_required()
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(user=request.user, item=item, order_completed=False)
    cart_qs = ShoppingCart.objects.filter(user=request.user, ordered=False)

    if cart_qs.exists():
        cart = cart_qs[0]
        if not created:
            order_item.quantity += 1
            order_item.save()
            cart.save()
            messages.info(request, f"{order_item.item.title.title()} added, {order_item.quantity} in cart ")
        else:
            cart.items.add(order_item)
            cart.save()
            messages.info(request, f"{order_item.item.title.title()} added, {order_item.quantity} in cart ")
    else:
        cart = ShoppingCart.objects.create(user=request.user)
        cart.items.add(order_item)
        cart.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))