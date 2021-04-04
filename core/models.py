from django.db import models
from django.contrib.auth.models import User
import random, string
from django.urls import reverse


def slug_generator():
    return ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))


class Categories(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='img/categories', null=True, blank=True)
    image_big = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class SubCategories(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent_category = models.ForeignKey(Categories, on_delete=models.CASCADE)

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


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

