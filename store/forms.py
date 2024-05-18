from django import forms

class FilterForm(forms.Form):
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)
    size_filter = forms.ChoiceField(choices=[('','Select Size'),('M','M'),('L','L'),('XL','XL'),('XXL','XXL')], required=False)
