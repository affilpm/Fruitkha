from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Assuming CustomUser is your custom user model
import re
from .models import Category, Product, Offer
from django.utils.translation import gettext_lazy as _
import re
from .models import Address
from orders.models import Coupon





class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user
    
    def clean_username(self): 
        username = self.cleaned_data['username']
    
        if username.isdigit():
            raise forms.ValidationError("Username cannot consist only of numbers.")

        if not re.match(r'^[\w.@+-]+$', username):
            raise forms.ValidationError("Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.")

        if not any(char.isalpha() for char in username):
            raise forms.ValidationError("Username must contain at least one alphabetical character.")

        if len(username) < 3: 
            raise forms.ValidationError("Username must be at least 3 characters long.")

        return username
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        
        if len(phone) < 8:
            raise forms.ValidationError("Phone number must be at least 8 digits long.")
        
        return phone


# forms.py



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'street', 'city', 'state', 'country', 'postal_code', 'phone_number']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not isinstance(name, str) or name.strip() == '':
            raise forms.ValidationError("Please enter a valid name.")
        return name

    def clean_street(self):
        street = self.cleaned_data.get('street')
        if not isinstance(street, str) or street.strip() == '':
            raise forms.ValidationError("Please enter a valid street.")
        return street

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not isinstance(city, str) or city.strip() == '':
            raise forms.ValidationError("Please enter a valid city.")
        return city

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if not isinstance(state, str) or state.strip() == '':
            raise forms.ValidationError("Please enter a valid state.")
        return state

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not isinstance(country, str) or country.strip() == '':
            raise forms.ValidationError("Please enter a valid country.")
        return country

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if not isinstance(postal_code, str) or not postal_code.isdigit():
            raise forms.ValidationError("Please enter a valid postal code (only digits).")
        if len(postal_code) != 6:  # Assuming postal code should be 6 digits
            raise forms.ValidationError("Postal code should be exactly 6 digits.")
        return postal_code

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not isinstance(phone_number, str) or not phone_number.isdigit():
            raise forms.ValidationError("Please enter a valid phone number (only digits).")
        if len(phone_number) < 8 or len(phone_number) > 15:  # Assuming phone number length constraints
            raise forms.ValidationError("Phone number should be between 8 and 15 digits.")
        return phone_number




class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_listed']  

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}), 
            'is_listed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Category Name',
            'description': 'Description',  
            'is_listed': 'Listed',
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.lower() if name else name

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if name:
            existing_names = Category.objects.filter(name__iexact=name)
            if existing_names.exists():
                self.add_error('name', 'Category with this name already exists.')
        return cleaned_data




class ProductForm(forms.ModelForm):
    offer = forms.ModelChoiceField(queryset=Offer.objects.all(), required=False, empty_label="No Offer")
    related_products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple, 
        label="Related Products"
    )
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'image1', 'image2', 'image3', 'price', 'stock', 'is_listed', 'offer', 'related_products']
        widgets = {
            'stock': forms.TextInput(attrs={'placeholder': 'Enter stock (kg)', 'class': 'form-control'}),
            'price': forms.TextInput(attrs={'placeholder': 'Enter price ($)', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].label += ' (kg)'
        self.fields['price'].label += ' ($)'

        if self.instance.pk:
            self.fields['related_products'].queryset = Product.objects.exclude(pk=self.instance.pk)
        else:
            self.fields['related_products'].queryset = Product.objects.all()
            
    def clean_name(self):
        name = self.cleaned_data['name']
        return name.lower() if name else name

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if name:
            existing_names = Product.objects.filter(name__iexact=name)
            if self.instance and self.instance.pk:
                existing_names = existing_names.exclude(pk=self.instance.pk)
            if existing_names.exists():
                self.add_error('name', 'A product with this name already exists.')
        return cleaned_data




class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_amount', 'minimum_required' ,'valid_from', 'valid_to', 'is_active']
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'valid_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            
        }
        






class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['name', 'description', 'discount_percentage', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean_name(self):
        name = self.cleaned_data['name']
        return name.lower() if name else name

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if name:
            existing_offers = Offer.objects.filter(name__iexact=name)
            if self.instance and self.instance.pk:
                existing_offers = existing_offers.exclude(pk=self.instance.pk)
            if existing_offers.exists():
                self.add_error('name', 'An offer with this name already exists.')
        return cleaned_data

