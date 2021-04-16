from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic
from RetailShopDjango.mixins import ProfileUpdateMixin
from users.forms import  UserBillingEditForm
from .forms import AddToCartForm
from users.models import UserProfile
from .models import Item, Categories, OrderItem, ShoppingCart, Coupons


class HomeView(generic.ListView):
    model = Categories
    context_object_name = 'categories'
    template_name = 'home.html'
     # paginate_by = 8
    ordering = 'pk'


class CartView(LoginRequiredMixin, generic.ListView):
    # model = ShoppingCart
    context_object_name = 'cart'
    template_name = 'cart.html'

    def get_queryset(self):
        try:
            qs = ShoppingCart.objects.get(user_id=self.request.user.id, ordered=False)
            return qs
        except ObjectDoesNotExist:
            messages.info(self.request, 'No items in cart')


class ProductDetailView(generic.DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'detail.html'

    def get_context_data(self, *args, **kwargs):
        form = AddToCartForm()
        item = Item.objects.get(slug=self.kwargs['slug'])
        items = Item.objects.filter(category__pk=item.category.pk).exclude(pk=item.pk)
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['items'] = items
        context['form'] = form
        return context


@login_required()
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
        return JsonResponse(data, safe=False)


# @login_required()
def add_to_cart_multiple(request, slug):
    if  request.user.is_authenticated:
        try:
            number = request.POST['item_quantity']
        except MultiValueDictKeyError:
            number = 1
        item = get_object_or_404(Item, slug=slug)
        order_item, created = OrderItem.objects.get_or_create(
            user=request.user,
            item=item,
            order_completed=False,
            )
        cart_qs = ShoppingCart.objects.filter(user=request.user, ordered=False)

        if cart_qs.exists():
            cart = cart_qs[0]
            if not created:
                order_item.quantity += int(number)
                order_item.save()
                messages.info(request, f"{order_item.item.title.title()} added, {order_item.quantity} in cart ")
            else:
                order_item.quantity = int(number)
                order_item.save()
                cart.items.add(order_item)
                cart.save()
                messages.info(request, f"{order_item.item.title.title()} added, {order_item.quantity} in cart ")
        else:
            cart = ShoppingCart.objects.create(user=request.user)
            cart.items.add(order_item)
            cart.save()
            messages.info(request, f"{order_item.item.title.title()} added, {order_item.quantity} in cart ")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return redirect('account_login')


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
            if not str(request.META.get('HTTP_REFERER')).endswith('cart/'):
                messages.info(request, f"{order_item.item.title.title()} added, {order_item.quantity} in cart ")
        else:
            cart.items.add(order_item)
            cart.save()
            if not str(request.META.get('HTTP_REFERER')).endswith('cart/'):
                messages.info(request, f"{order_item.item.title.title()} added, {order_item.quantity} in cart ")
    else:
        cart = ShoppingCart.objects.create(user=request.user)
        cart.items.add(order_item)
        cart.save()
        messages.info(request, f"{order_item.item.title.title()} added, {order_item.quantity} in cart ")
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required()
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get(user=request.user, item=item, order_completed=False)
    cart_qs = ShoppingCart.objects.filter(user=request.user, ordered=False)
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        cart = cart_qs[0]
        cart.items.remove(order_item)
        order_item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def remove_order_item(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get(user=request.user, item=item, order_completed=False)
    cart_qs = ShoppingCart.objects.filter(user=request.user, ordered=False)
    cart = cart_qs[0]
    cart.items.remove(order_item)
    order_item.delete()
    return redirect('core:cart_view')


def add_coupon(request):
    if request.POST:
        code = request.POST['code']
        try:
            coupon = Coupons.objects.get(name=code, valid=True)
            order = ShoppingCart.objects.get(user=request.user, ordered=False)
            order.coupon = coupon
            order.save()
            messages.success(request, 'Code Confirmed')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

        except ObjectDoesNotExist:
            messages.warning(request, 'Invalid Coupon code')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    pass


def remove_coupon(request):
    order = ShoppingCart.objects.get(user=request.user, ordered=False)
    order.coupon = None
    order.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def ajax_search(request):
    search_string = request.GET.get('searchTxt')
    search_result = Item.objects.filter(title__icontains=search_string) \
        | Item.objects.filter(price__startswith=search_string) \
        | Item.objects.filter(description__icontains=search_string) \
        | Item.objects.filter(category__name__icontains=search_string)
    data = search_result.values()
    return render(request, 'search_results.html', {'results': search_result})
    # return JsonResponse(list(data), safe=False)


def ajax_load_products(request, display):
    display = int(request.GET.get('display'))
    items = Item.objects.all().order_by('pk')[0:display]
    return render(request, 'product_loader.html', {'items': items})


class UserBillingView(ProfileUpdateMixin, SuccessMessageMixin, generic.UpdateView,):
    model = UserProfile
    form_class = UserBillingEditForm
    success_url = reverse_lazy('core:home')
    template_name = 'checkout.html'

    # def get_success_url(self, **kwargs):
    #     return reverse('core:checkout', kwargs={
    #         'pk': str(self.request.user.id)
    #     })

    def get_context_data(self, **kwargs):
        try:
            cart = ShoppingCart.objects.get(user_id=self.request.user.id, ordered=False)
            context = super(UserBillingView, self).get_context_data(**kwargs)
            context['cart'] = cart
            return context
        except ObjectDoesNotExist:
            context = super(UserBillingView, self).get_context_data(**kwargs)
            return context

    def form_valid(self, form):
        try:
            cart = ShoppingCart.objects.get(user_id=self.request.user.id, ordered=False)
            cart.ordered = True
            cart.ordered_date = timezone.now()
            cart.save()
            order_item_qs = OrderItem.objects.filter(user=self.request.user, order_completed=False)
            for order_item in order_item_qs:
                order_item.item.warehouse_quantity -= order_item.quantity
                order_item.item.save()
                order_item.order_completed = True
                order_item.save()
            messages.info(self.request, "Order Confirmed")
            return super().form_valid(form)
        except ObjectDoesNotExist:
            messages.info(self.request, "You don't have an active order")
            return redirect('core:home')

