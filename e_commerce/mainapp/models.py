
from django.db import models
import datetime
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
# ------------------------------------------------------------------------------

class CheckOut(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    country = CountryField(multiple=False)
    street_address = models.CharField(max_length=255)
    apartment_address = models.CharField(max_length=255)
    phone_number = models.IntegerField()    
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
# ------------------------------------------------------------------------------

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date =  models.DateTimeField(default=datetime.datetime.now(), blank=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username        
# ------------------------------------------------------------------------------

class Tag(models.Model):
    name= models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)
# ------------------------------------------------------------------------------

class ProductTag(models.Model):
    tag = models.ManyToManyField(to='Tag')
    product = models.OneToOneField(to='Item', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product) + ' ' + str('#')
