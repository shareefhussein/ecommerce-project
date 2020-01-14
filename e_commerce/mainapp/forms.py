from django import forms
from django.forms.models import ModelForm
from mainapp.models import Order, CheckOut

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = CheckOut
        exclude = []
   