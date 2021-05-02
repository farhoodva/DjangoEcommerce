import stripe
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from RetailShopDjango.mixins import ProfileUpdateMixin
from users.forms import UserBillingEditForm
from .forms import AddToCartForm
from users.models import UserProfile
from .models import Item, Categories, OrderItem, ShoppingCart, Coupons, SubCategories, Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def ajax_load_products(request, display):
    # display = request.GET.get('display')
    items = Item.objects.all().order_by('pk')[display:display+4]
    return render(request, 'product_loader.html', {'items': items})


class HomeView(generic.View):
    def get(self, display):
        display = 4  # initial number of items
        context = {
            'items': Item.objects.all().order_by('pk')[0:display],
            'categories': Categories.objects.all()
        }
        return render(self.request, 'home.html', context)


class CartView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'cart'
    template_name = 'cart.html'

    def get_queryset(self):
        try:
            qs = ShoppingCart.objects.get(user_id=self.request.user.id, status='New')
            return qs
        except ObjectDoesNotExist:
            messages.info(self.request, 'You have no active cart')


class PurchaseHistoryView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'carts'
    template_name = 'purchase_history.html'

    def get_queryset(self):
        try:
            qs = ShoppingCart.objects.filter(user_id=self.request.user.id, status='Paid')
            return qs
        except ObjectDoesNotExist:
            messages.info(self.request, 'You have no orders')


def cart_detail_view(request, pk):
    try:
        cart = ShoppingCart.objects.get(pk=pk)
    except ObjectDoesNotExist:
        messages.warning(request, 'Order does not exist')
        return redirect('core:home')


class ShopView(generic.ListView):
    model = SubCategories
    context_object_name = 'sub_categories'
    template_name = 'shop.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        items = Item.objects.all()
        categories = Categories.objects.all()
        context = super(ShopView, self).get_context_data(**kwargs)
        context['categories'] = categories
        context['items'] = items
        return context


class SubCatView(generic.ListView):
    context_object_name = 'items'
    template_name = 'shop_sub_category.html'

    def get_queryset(self):
        try:
            sub_cat = SubCategories.objects.get(id=self.kwargs['pk'])
            items = Item.objects.filter(category=sub_cat)
            return items
        except ObjectDoesNotExist:
            return Item.objects.all()[0:30]

    def get_context_data(self, *, object_list=None, **kwargs):
        try:
            sub_cat_name = SubCategories.objects.get(id=self.kwargs['pk']).name
        except ObjectDoesNotExist:
            sub_cat_name = 'shop'
        sub_categories = SubCategories.objects.all()
        categories = Categories.objects.all()
        context = super(SubCatView, self).get_context_data(**kwargs)
        context['categories'] = categories
        context['sub_categories'] = sub_categories
        context['sub_cat_name'] = sub_cat_name
        return context


class CatView(generic.ListView):
    context_object_name = 'items'
    template_name = 'shop_cat_view.html'

    def get_queryset(self):
        try:
            cat = Categories.objects.get(id=self.kwargs['pk'])
            items = Item.objects.filter(category__parent_category=cat)
            return items
        except ObjectDoesNotExist:
            return Item.objects.all()[0:30]

    def get_context_data(self, *, object_list=None, **kwargs):
        try:
            cat_name = Categories.objects.get(id=self.kwargs['pk']).name
        except ObjectDoesNotExist:
            cat_name = 'shop'
        sub_categories = SubCategories.objects.all()
        categories = Categories.objects.all()
        context = super(CatView, self).get_context_data(**kwargs)
        context['categories'] = categories
        context['sub_categories'] = sub_categories
        context['cat_name'] = cat_name
        return context


class UserBillingView(ProfileUpdateMixin, SuccessMessageMixin, generic.UpdateView,):
    model = UserProfile
    form_class = UserBillingEditForm
    success_url = reverse_lazy('core:home')
    template_name = 'checkout.html'

    def get_context_data(self, *args, **kwargs):
        try:
            cart = ShoppingCart.objects.get(user_id=self.request.user.id, status='New')
            context = super(UserBillingView, self).get_context_data(**kwargs)
            context['cart'] = cart
            return context
        except ObjectDoesNotExist:
            context = super(UserBillingView, self).get_context_data(**kwargs)
            return context

    def form_valid(self, form):
        try:
            cart = ShoppingCart.objects.get(user_id=self.request.user.id, status='New')
            if form.cleaned_data['payment_method'] == 'Stripe':
                super().form_valid(form)
                context = {
                    'cart': cart,
                    'stripe': settings.STRIPE_PUBLISHABLE_KEY
                }
                # cart.status = 'Checked-out'
                cart.ordered_date = timezone.now()
                cart.save()
                return render(self.request, 'payment.html', context)

            elif form.cleaned_data['payment_method'] == 'Paypal':
                super().form_valid(form)
                # cart.status = 'Checked-out'
                cart.ordered_date = timezone.now()
                cart.save()
                context = {
                    'cart': cart
                }
                return render(self.request, 'paypal_payment.html', context)
            else:
                cart.status = 'New'
                cart.save()
                messages.info(self.request, 'Invalid payment method')
                return redirect('core:checkout', self.request.user.id)

        except ObjectDoesNotExist:
            messages.info(self.request, "You don't have an active order")
            return redirect('core:home')


class CreateCheckoutSession(generic.View):
    def post(self, request, *args, **kwargs):
        try:
            your_domain = 'http://127.0.0.1:8000'
            cart = ShoppingCart.objects.get(pk=self.kwargs['pk'])
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(cart.get_total_order_price()*100),
                            'product_data': {
                                'name': 'Total order amount:',
                                # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                            },
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    'user_id': self.request.user.id,
                    'cart_pk': self.kwargs['pk']
                },
                mode='payment',
                success_url=your_domain + '/home',
                cancel_url=your_domain + '/home',
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}), 403


@csrf_exempt
def stripe_webhook(request):
    print(1)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print(123)
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        cart = ShoppingCart.objects.get(pk=session['metadata'].cart_pk, status='New')
        cart.status = 'Paid'
        payment = Payment.objects.create(
            payment_type='stripe',
            charge_id=session['payment_intent'],
            user=cart.user,
            amount=cart.get_total_order_price(),
            )
        payment.save()
        cart.payment = payment
        cart.save()
        order_item_qs = OrderItem.objects.filter(user_id=session['metadata'].user_id, order_completed=False)
        for order_item in order_item_qs:
            order_item.item.warehouse_quantity -= order_item.quantity
            order_item.item.save()
            order_item.order_completed = True
            order_item.save()
        customer_email = cart.user.email
        send_mail(
            'FSTORE',
            f'You can check your order details in your profile using your order reference code:{cart.ref_code} ',
            'from@example.com',
            [customer_email],
            fail_silently=False,
        )
    return HttpResponse(status=200)


def paypal_checkout_complete(request, pk):
    cart = ShoppingCart.objects.get(pk=pk)
    cart.status = 'Paid'
    payment = Payment.objects.create(
        payment_type='stripe',
        charge_id=cart.id,  # TODO: find out how to add paypal charge id
        user=cart.user,
        amount=cart.get_total_order_price(),
    )
    payment.save()
    cart.save()
    order_item_qs = OrderItem.objects.filter(user_id=cart.user_id, order_completed=False)
    for order_item in order_item_qs:
        order_item.item.warehouse_quantity -= order_item.quantity
        order_item.item.save()
        order_item.order_completed = True
        order_item.save()
    return HttpResponse(status=200)


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
    if request.user.is_authenticated:
        try:
            number = request.POST['item_quantity']
        except MultiValueDictKeyError:
            number = 1
        try:
            item = Item.objects.get(slug=slug)
            order_item, created = OrderItem.objects.get_or_create(
                user=request.user,
                item=item,
                order_completed=False,
            )
            cart_qs = ShoppingCart.objects.filter(user=request.user, status='New')
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
        except ObjectDoesNotExist:
            pass
    return redirect('account_login')


@login_required()
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(user=request.user, item=item, order_completed=False)
    cart_qs = ShoppingCart.objects.filter(user=request.user, status='New')

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
    cart_qs = ShoppingCart.objects.filter(user=request.user, status='New')
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
    order_item = get_object_or_404(OrderItem, user=request.user, item=item, order_completed=False)
    cart_qs = ShoppingCart.objects.filter(user=request.user, status='New')
    cart = cart_qs[0]
    cart.items.remove(order_item)
    order_item.delete()
    return redirect('core:cart_view')


def add_coupon(request):
    if request.POST:
        code = request.POST['code']
        try:
            coupon = Coupons.objects.get(name=code, valid=True)
            order = ShoppingCart.objects.get(user=request.user, status='New')
            order.coupon = coupon
            order.save()
            messages.success(request, 'Code Confirmed')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

        except ObjectDoesNotExist:
            messages.warning(request, 'Invalid Coupon code')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    pass


def remove_coupon(request):
    order = ShoppingCart.objects.get(user=request.user, status='New')
    order.coupon = None
    order.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def search(request):
    if request.is_ajax():
        search_string = request.GET.get('searchTxt')
        search_results_qs = Item.objects.filter(title__icontains=search_string) \
            | Item.objects.filter(price__startswith=search_string) \
            | Item.objects.filter(description__icontains=search_string) \
            | Item.objects.filter(category__name__icontains=search_string)
        # data = search_results_qs.values()
        return render(request, 'search_results_ajax.html', {'results': search_results_qs})
    else:
        sub_categories = SubCategories.objects.all()
        categories = Categories.objects.all()
        try:
            search_string = request.POST.get('searchTxt')
            search_results_qs = Item.objects.filter(title__icontains=search_string) \
                | Item.objects.filter(price__startswith=search_string) \
                | Item.objects.filter(description__icontains=search_string) \
                | Item.objects.filter(category__name__icontains=search_string)
            context = {
                'results': search_results_qs,
                'sub_categories': sub_categories,
                'categories': categories
            }
            return render(request, 'search_results.html', context)
        except ValueError:
            return redirect('core:home')
