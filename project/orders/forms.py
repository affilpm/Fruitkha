from django import forms
from .models import CancellationRequest


# class ApplyCouponForm(forms.Form):
#     code = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Enter coupon code'
#     }))
    

class CouponApplyForm(forms.Form):
    code = forms.CharField(label='Coupon Code', max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter coupon code'}))




class CancellationRequestForm(forms.ModelForm):
    class Meta:
        model = CancellationRequest
        fields = ['reason']
