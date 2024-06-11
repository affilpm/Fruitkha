from django import forms
from orders.models import Coupon



class CartUpdateForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1)
    
class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())

       




