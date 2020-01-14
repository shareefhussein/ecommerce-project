
from django.db import models
import datetime
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import os 
from django.contrib.auth.models import User

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class CheckOut(models.Model):
    user = models.ForeignKey(to =settings.AUTH_USER_MODEL, 
                            on_delete= 'CASCADE', null=True)
    street_address = models.CharField(max_length=255)
    apartment_address = models.CharField(max_length=255)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
# ------------------------------------------------------------------------------
class Category(models.Model):
    title = models.CharField(max_length=300)
    primaryCategory = models.BooleanField(default=False)

    def __str__(self):
        return self.title
# ------------------------------------------------------------------------------
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to= 'img', blank= True)

    def __str__(self):
        return self.title  
# ------------------------------------------------------------------------------
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    @property
    def get_total_item_price(self):
        return self.quantity * self.item.price 

    @property
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    @property    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


# ------------------------------------------------------------------------------
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date =  models.DateTimeField(default=datetime.datetime.now(), blank=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @property
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total            
# ------------------------------------------------------------------------------
class Tag(models.Model):
    name= models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)
# ------------------------------------------------------------------------------
class ProductTag(models.Model):
    tag = models.ManyToManyField(to='Tag')
    product = models.OneToOneField(to='Item', on_delete=models.CASCADE)

    @classmethod
    def export_to_csv(cls, path):
        all_products = ProductTag.objects.all()

    def __str__(self):
        return str(self.product) + ' ' + str('#')
