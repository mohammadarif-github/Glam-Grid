from django import forms
from .models import Order

class BillingForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','email','phone','address','city','state',]