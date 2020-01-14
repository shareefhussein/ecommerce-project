from django.contrib import admin
from mainapp.models import Item, Order, OrderItem, Category, ProductTag, Tag, CheckOut


admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProductTag)
admin.site.register(Tag)
admin.site.register(CheckOut)


