from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from home.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from home.models import Product
from cart.models import Cart
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect, reverse
from .models import Wishlist



#################not superuser###########################################################################################################################
def is_not_superuser(user):
    return not user.is_superuser






def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user) 
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})






@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
def add_to_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        Wishlist.objects.get_or_create(user=request.user, product=product)
        return redirect('single_product', product_id=product.id)
    
    
    

@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
def remove_from_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        wishlist_item = Wishlist.objects.get(user=request.user, product=product)
        wishlist_item.delete()
        return redirect('single_product', product_id=product.id)
       







@user_passes_test(lambda u: not u.is_superuser, login_url='user_login')
@never_cache
@require_POST
def wishlist_to_cart(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    Wishlist.objects.filter(user=request.user, product=product).delete()
    
    return redirect('wishlist')