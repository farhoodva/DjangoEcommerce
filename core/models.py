from django.db import models
from django.contrib.auth.models import User


class Categories(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='img/categories', null=True, blank=True)

    def __str__(self):
        return self.name


class SubCategories(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent_category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField
    warehouse_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.title


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

