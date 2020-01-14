from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from .models import Item, OrderItem, Order, Category,Tag ,ProductTag, CheckOut
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from mainapp.forms import CheckoutForm
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


class CheckOutCreateView(CreateView):
    model = CheckOut
    template_name = 'checkout.html'
    success_url = reverse_lazy('thank_you')
    fields= ['street_address', 'apartment_address', 'zip', 'address_type']
# ------------------------------------------------------------------------------
def thank_you(request):
    return render(request, 'thank_you.html')    
# ------------------------------------------------------------------------------
class HomeListView(ListView):
    model = Item
    template_name = "home.html" 
# ------------------------------------------------------------------------------
class BaseListView(ListView):
    model = Item
    template_name = 'base.html'    
# ------------------------------------------------------------------------------
class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"
# ------------------------------------------------------------------------------
@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user)
    order_qs = Order.objects.filter(user=request.user)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("product", pk)
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("product", pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("product", pk)
# ------------------------------------------------------------------------------
class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
# ------------------------------------------------------------------------------
@login_required
def remove_from_cart(request, pk):
    if request.method=="POST":
        cart_item = OrderItem.objects.get(id=pk)
        cart_item.delete()       
        messages.info(request, "This item was removed from your cart.")
        return redirect("order_register")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("order_register")
# ------------------------------------------------------------------------------
class SearchResultsView(ListView):
    model = Item
    template_name = 'search_results.html'
    
    def get_queryset(self): 
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(title__contains=query )
        return object_list
# ------------------------------------------------------------------------------
class OrderListView(ListView):
    model = OrderItem
    template_name = 'order.html'
    success_url = reverse_lazy('order_register')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = OrderItem.objects.filter(user=self.request.user, ordered=False)
        return context
# ---------------------------------------------------------------------
class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    fildes="__all__"
# ---------------------------------------------------------------------
def ItemsListView(request,pk):
    context={}
    product = Item.objects.filter(category=pk)
    context['Products'] = product
    return render(request,"category_details.html",context=context) 
# ---------------------------------------------------------------------
