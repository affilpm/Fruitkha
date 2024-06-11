from django.contrib import admin
from .models import Category, Product, CustomUser, Address, Offer


# Register your models here.
from .forms import ProductForm
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Address)
admin.site.register(Offer)

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ['name', 'price', 'stock', 'is_listed']
    list_filter = ['is_listed', 'category']
    search_fields = ['name', 'description']
    filter_horizontal = ('related_products',) 

admin.site.register(Product, ProductAdmin)
