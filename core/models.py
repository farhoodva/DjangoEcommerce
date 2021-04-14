import secrets
import random, string
from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile
from django.db.models.signals import post_save
from django.urls import reverse


def slug_generator():
    return ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))


class Categories(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='img/categories', null=True, blank=True)
    image_big = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class SubCategories(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent_category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'SubCategories'

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to='img/Items')
    image_2 = models.ImageField(upload_to='img/Items', null=True, blank=True)
    image_3 = models.ImageField(upload_to='img/Items', null=True, blank=True)
    image_4 = models.ImageField(upload_to='img/Items', null=True, blank=True)
    discount_price = models.FloatField(blank=True, null=True)
    warehouse_quantity = models.PositiveIntegerField()
    description = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(SubCategories, on_delete=models.SET_DEFAULT, default=1)
    wishlist = models.ManyToManyField(User, related_name='wishlist', blank=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator()
            super(Item, self).save()
        super(Item, self).save()

    def __str__(self):
        return self.title

    def get_item_detail_url(self):
        return reverse('core:product_detail', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('core:add_to_cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('core:remove_from_cart', kwargs={
            'slug': self.slug
        })

    def get_remove_order_item_url(self):
        return reverse('core:remove_order_item', kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.quantity} of {self.item.title} "

    def total_price(self):
        return self.item.price * self.quantity


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_info = models.ForeignKey('users.UserProfile', on_delete=models.SET_NULL, null=True, blank=True)
    items = models.ManyToManyField(OrderItem)
    coupon = models.ForeignKey('core.Coupons', on_delete=models.SET_NULL, null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.shipping_info:
            self.shipping_info = UserProfile.objects.get(user=self.user)
            super(ShoppingCart, self).save()
        super(ShoppingCart, self).save()

    def __str__(self):
        return self.user.username

    def get_total_order_price(self):
        total = 0
        order_qs = self.items.all()
        for order_item in order_qs:
            total += order_item.total_price()
        if self.coupon:
            if not self.coupon.percentage:
                return total - self.coupon.amount
            else:
                return int(total - total / self.coupon.amount)
        else:
            return total


class Coupons (models.Model):
    name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    amount = models.PositiveIntegerField()
    percentage = models.BooleanField(default=False)
    valid = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Coupons'

    def __str__(self):
        if self.percentage:
            return f"{self.name} for {self.amount}% "
        return f"{self.name} for ${self.amount}"

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):

        if created:
            id_string = str(instance.id)
            upper_alpha = "ABCDEFGHJKLMNPQRSTVWXYZ"
            # random_str = "".join(secrets.choice(upper_alpha, k=8))
            random_str = "".join(secrets.choice(upper_alpha) for i in range(8))
            instance.name = (random_str + id_string)[-8:]
            instance.save()


post_save.connect(Coupons.post_create, sender=Coupons)

