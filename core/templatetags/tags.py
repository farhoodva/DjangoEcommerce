from django import template
from django.core.exceptions import ObjectDoesNotExist

from core.models import ShoppingCart, Item
register = template.Library()


@register.filter()
def count_order(user):
    order_qs = ShoppingCart.objects.filter(user=user, ordered=False)
    if order_qs.exists():
        order_qs = order_qs[0]
        return order_qs.items.count()
    else:
        return 0


@register.filter()
def count_wishlist(user):
    try:
        wishlist = Item.objects.filter(wishlist__username=user.username)
    except ObjectDoesNotExist:
        return 0
    return wishlist.count()