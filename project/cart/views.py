from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from .models import Cart
from home.models import Product
from .forms import CartUpdateForm
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache
# Create your views here.



#################not superuser###########################################################################################################################
def is_not_superuser(user):
    return not user.is_superuser
###########cart#####################cart######################cart##############################cart####################cart################
  



 

@user_passes_test(is_not_superuser, login_url='user_login')
@never_cache
def cart(request):
    cart_items = Cart.objects.filter(user=request.user, product__is_listed=True).order_by('id')
    total_cost = 0  
    total_original_cost = 0 

    if request.method == 'POST':
        form = CartUpdateForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']
            cart_item = Cart.objects.filter(user=request.user, product_id=product_id).first()
            if cart_item:
                old_quantity = cart_item.quantity
                cart_item.quantity = quantity
                cart_item.save()
                cart_item.subtotal = cart_item.product.price * cart_item.quantity
                cart_item.save()
                total_cost -= cart_item.product.price * old_quantity
                total_cost += cart_item.subtotal
            return JsonResponse({'success': True, 'total_cost': total_cost})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CartUpdateForm()

    cart_items = cart_items.exclude(quantity__lte=0)

    for item in cart_items:
        product = item.product
        if product.stock <= 0 or not product.is_listed:
            item.available = False
            item.save()
            item.delete()
        else:
            item.available = True
            item.save()
            item.subtotal = product.price * item.quantity
            total_cost += item.subtotal  
            
            original_price = product.original_price or product.price  # Use original price if available, otherwise use current price
            item.original_price_total = original_price * item.quantity  # Store the original price total for the item
            total_original_cost += item.original_price_total
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'form': form, 'total_cost': total_cost})


from django.shortcuts import redirect, reverse






@user_passes_test(is_not_superuser, login_url='user_login')
@never_cache
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart_item, created = Cart.objects.get_or_create(user=request.user, product_id=product_id)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect(reverse('single_product', args=[product_id]))
    else:
        pass




@user_passes_test(is_not_superuser, login_url='user_login')
def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            try:
                cart_item = Cart.objects.get(user=request.user, product_id=product_id)
                cart_item.delete()
                return JsonResponse({'success': True})
            except Cart.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Item not found in the cart.'})
        else:
            return JsonResponse({'success': False, 'error': 'Product ID is missing.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})

    
