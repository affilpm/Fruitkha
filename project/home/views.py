from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .forms import CategoryForm, ProductForm, UserRegistrationForm
from .models import Category, Product, CustomUser, Offer
from cart.models import Cart
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings as condrib_settings
import random
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.http import JsonResponse
from orders.models import Order, OrderItem
from cart.forms import CartUpdateForm
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import update_session_auth_hash
import re
from django.shortcuts import render, redirect
from .models import Address
from .forms import AddressForm
from django.shortcuts import render
from .models import Address 
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegistrationForm
from .utils import send_sms
import random
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from orders.models import Coupon, Wallet, Transaction, CancellationRequest
from .forms import CouponForm, OfferForm
from wishlist.models import Wishlist
from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from datetime import datetime, timedelta
from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime, timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
import io
from orders.models import CancellationRequest
import xlsxwriter # type: ignore
from django.db.models import Sum
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay, TruncHour
from django.db.models import Count
import string
from django.template.loader import render_to_string
import io
from django.utils import timezone
import time
from openpyxl import Workbook



#################not superuser###########################################################################################################################
def is_not_superuser(user):
    return not user.is_superuser




#############home  ####################################home ############################home############################3  

@never_cache
def home(request):
    
    products = Product.objects.all()
    categories = Category.objects.all()

    products = Product.objects.filter(stock__gt=0)[:6]
    
    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'home.html', context)





######shop######shop######shop######shop######shop######shop######shop######shop######shop

@never_cache
def shop(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_listed=True)

    search_name = request.GET.get('search_name')
    filter_category = request.GET.get('filter_category')
    sort_price = request.GET.get('sort_price')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if search_name:
        products = products.filter(name__icontains=search_name)
    if filter_category:
        products = products.filter(category__name=filter_category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if sort_price == 'lowest_to_highest':
        products = products.order_by('price')
    elif sort_price == 'highest_to_lowest':
        products = products.order_by('-price')

    return render(request, 'shop.html', {'products': products, 'categories': categories})





######################about######################about######################about######################about#####
 
@never_cache
def about(request):
    return render(request, 'about.html')
   
   
   
   
   
####################customer_service####################customer_service####################customer_service#######
    
@never_cache
def customer_service(request):
    return render(request, 'contact.html')





#########address#############################address###########################address########################################################


@user_passes_test(is_not_superuser, login_url='user_login')
@never_cache
def address(request):
    addresses = Address.objects.filter(user=request.user).order_by('id')
    return render(request, 'addresses.html', {'addresses': addresses})





@user_passes_test(is_not_superuser, login_url='user_login')
@never_cache
def add_address(request):

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('address')   
    else:
        form = AddressForm()
    return render(request, 'add_address.html', {'form': form})




@user_passes_test(is_not_superuser, login_url='user_login')
@never_cache
def edit_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully.')
            return redirect('address')  # Redirect to the address page
    else:
        form = AddressForm(instance=address)

    # Check if the user came from the checkout page
    came_from_checkout = request.GET.get('checkout') == 'true'
    
    return render(request, 'edit_address.html', {'form': form, 'address': address, 'came_from_checkout': came_from_checkout})










@user_passes_test(is_not_superuser, login_url='user_login')
def delete_address(request, address_id):
    address = Address.objects.get(pk=address_id)
    if request.method == 'POST':
        address.delete()
        return redirect('address')  # Redirect to the address page after deletion
    return render(request, 'address.html', {'address': address})







 
###################################sigle product#######################sigle product########################sigle product############






def single_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_listed=True)

    out_of_stock = product.stock <= 0
    
    product_in_cart = False
    if request.user.is_authenticated:
        product_in_cart = Cart.objects.filter(user=request.user, product_id=product_id).exists()
    
    product_in_wishlist = False
    if request.user.is_authenticated:
        product_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    related_products = product.related_products.filter(is_listed=True)

    breadcrumbs = [
        {'title': 'Home', 'url': reverse('home')},
        {'title': product.name, 'url': reverse('single_product', args=[product_id])}
    ]
    previous_page_url = request.META.get('HTTP_REFERER')

    context = {
        'product': product,
        'related_products': related_products,
        'out_of_stock': out_of_stock,
        'product_in_wishlist': product_in_wishlist,
        'breadcrumbs': breadcrumbs,
        'previous_page_url': previous_page_url,
        'product_in_cart': product_in_cart,
    }

    return render(request, 'single_product.html', context)








###########################account#########################account#############################account######################account########################################


@user_passes_test(is_not_superuser, login_url='user_login')
@never_cache
def user_profile(request):
    user = request.user
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user, balance=0)
    return render(request, 'user_profile.html', {'user': user, 'wallet':wallet})





@user_passes_test(is_not_superuser, login_url='user_login')
@never_cache
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        
        if not is_strong_password(new_password):
            return JsonResponse({'success': False, 'message': 'Your new password is not strong enough. It must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.'})
        
        if new_password != confirm_new_password:
            return JsonResponse({'success': False, 'message': 'New password and confirm new password do not match.'})
        
        if not request.user.check_password(current_password):
            return JsonResponse({'success': False, 'message': 'Current password is incorrect.'})
        
        request.user.set_password(new_password)
        request.user.save()
        
        update_session_auth_hash(request, request.user)
        
        logout(request)
        
        return JsonResponse({'success': True, 'message': 'Password changed successfully. You have been logged out.'})
    
    return render(request, 'user_profile.html')




def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[!@#$%^&*()_+=-]", password):
        return False
    return True






@login_required(login_url='user_login')
def edit_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        if new_username:
            error_messages = validate_username(new_username)
            if error_messages:
                return JsonResponse({'success': False, 'errors': error_messages})
            elif new_username == request.user.username:
                return JsonResponse({'success': False, 'errors': ['New username cannot be the same as the current username.']})
            else:
                user = request.user
                user.username = new_username
                user.save()
                return JsonResponse({'success': True, 'message': 'Username updated successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': ['Please provide a valid username.']})
    else:
        return JsonResponse({'success': False, 'errors': ['Invalid request method.']})

def validate_username(username):
    error_messages = []
    if username.isdigit():
        error_messages.append("Username cannot consist only of numbers.")
    elif not re.match(r'^[\w.@+-]+$', username):
        error_messages.append("Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.")
    elif not any(char.isalpha() for char in username):
        error_messages.append("Username must contain at least one alphabetical character.")
    elif len(username) < 3:
        error_messages.append("Username must be at least 3 characters long.")
    elif CustomUser.objects.filter(username=username).exists():
        error_messages.append("Username already exists. Please choose a different one.")
    return error_messages




@login_required(login_url='user_login')
def edit_first_name(request):
    if request.method == 'POST':
        new_first_name = request.POST.get('new_first_name')
        if new_first_name:
            request.user.first_name = new_first_name
            request.user.save()
    return redirect('user_profile')





@login_required(login_url='user_login')
def edit_last_name(request):
    if request.method == 'POST':
        new_last_name = request.POST.get('new_last_name')
        if new_last_name:
            request.user.last_name = new_last_name
            request.user.save()
    return redirect('user_profile')

##################user register and login#########################user register and login#######user register and login########user register and login##########





@login_required(login_url='user_login')
@never_cache
def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('user_login')





OTP_EXPIRATION_TIME = 40  # seconds

@never_cache
def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['otp_timestamp'] = time.time()
            request.session['user_data'] = form.cleaned_data

            phone_number = form.cleaned_data['phone']
            message = f'Your OTP is: {otp}'
            success, response = send_sms(phone_number, message)
            if not success:
                messages.error(request, f'Failed to send OTP: {response}')
                return redirect('user_register')

            return redirect('otp')
    else:
        form = UserRegistrationForm()
    return render(request, 'user_register.html', {'form': form})




@never_cache
def otp(request):
    if 'otp' in request.session and 'otp_timestamp' in request.session:
        current_time = time.time()
        otp_creation_time = request.session['otp_timestamp']
        remaining_time = OTP_EXPIRATION_TIME - (current_time - otp_creation_time)
        if remaining_time <= 0:
            del request.session['otp']
            del request.session['otp_timestamp']
            messages.error(request, 'Your OTP has expired. Please click "Resend OTP" to receive a new OTP.')
            return render(request, 'otp.html', {'remaining_time': 0})
        
        if request.method == 'POST':
            otp_entered = request.POST.get('otp')
            if otp_entered == str(request.session['otp']):
                user_data = request.session.get('user_data')
                if user_data:
                    form = UserRegistrationForm(user_data)
                    if form.is_valid():
                        user = form.save(commit=False)
                        user.email = form.cleaned_data['email']
                        user.phone = form.cleaned_data['phone']
                        user.save()

                        del request.session['otp']
                        del request.session['otp_timestamp']
                        del request.session['user_data']

                        return redirect('user_login')
                else:
                    messages.error(request, 'User data is missing.')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
        return render(request, 'otp.html', {'remaining_time': int(remaining_time)})
    else:
        return redirect('user_register')




@never_cache
def resend_otp(request):
    if 'user_data' in request.session:
        user_data = request.session['user_data']
        phone_number = user_data.get('phone')
        if phone_number:
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['otp_timestamp'] = time.time()
            message = f'Your new OTP is: {otp}'
            success, response = send_sms(phone_number, message)
            if success:
                return JsonResponse({'success': True, 'remaining_time': OTP_EXPIRATION_TIME})
            else:
                return JsonResponse({'success': False, 'message': response})
    return JsonResponse({'success': False, 'message': 'User data not found in session.'})




@never_cache
def delete_otp(request):
    if 'otp' in request.session:
        del request.session['otp']
    if 'otp_timestamp' in request.session:
        del request.session['otp_timestamp']
    return JsonResponse({'success': True})





def user_login(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('home')  

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active and not user.is_superuser:
                    login(request, user)
                    return redirect('home')
                elif user.is_superuser:
                    messages.error(request, "Admin login is not allowed from this page.")
                else:
                    messages.error(request, "Your account is blocked. Please contact support for assistance.")
                    return render(request, 'user_login.html', {'form': form, 'blocked': True})
        else:
            messages.error(request, "Invalid username or password or Your account is inactive.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'user_login.html', {'form': form, 'blocked': False})








#####################admin dashboard################################admin dashboard##################admin dashboard#################admin dashboard############




@staff_member_required(login_url='admin_login')
@never_cache
def admin_dashboard(request):
    interval = request.GET.get('interval', 'day')

    if interval == 'month':
        start_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=32)
        trunc_func = TruncDay
        date_format = "%d-%m-%Y"
    elif interval == 'week':
        today = timezone.now()
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=7)
        trunc_func = TruncDay
        date_format = "%d-%m-%Y"
    elif interval == 'year':
        start_date = timezone.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date.replace(year=start_date.year + 1)
        trunc_func = TruncMonth
        date_format = "%m-%Y"
    else:  
        start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        trunc_func = TruncHour
        date_format = "%H:%M"

    orders = Order.objects.filter(order_date__gte=start_date, order_date__lt=end_date)
    order_count = orders.count()

    for order in orders:
        order.order_items = OrderItem.objects.filter(order=order)

    total_sales = orders.aggregate(total_sales=Sum('total_cost'))['total_sales'] or 0
    products_sold_count = OrderItem.objects.filter(order__in=orders).count()
    coupons_used_count = orders.exclude(coupon__isnull=True).count()

 
    orders_data = Order.objects.filter(order_date__gte=start_date, order_date__lt=end_date).annotate(period=trunc_func('order_date')).values('period').annotate(order_count=Count('id')).order_by('period')
    periods = [entry['period'].strftime(date_format) for entry in orders_data]
    orders_count = [entry['order_count'] for entry in orders_data]
    
    top_selling_products = OrderItem.objects.filter(order__in=orders).values('product__name').annotate(product_count=Count('id')).order_by('-product_count')[:10]
   
    top_selling_categories = Category.objects.annotate(product_count=Count('product__orderitem')).order_by('-product_count')[:10]
    context = {
        'total_sales': total_sales,
        'start_date': start_date,
        'end_date': end_date - timedelta(days=1),
        'interval': interval.capitalize(),
        'orders': orders,
        'products_sold_count': products_sold_count,
        'coupons_used_count': coupons_used_count,
        'orders_count': orders_count,
        'periods': periods,
        'order_count': order_count,
        'top_selling_products': top_selling_products,
        'top_selling_categories': top_selling_categories,
    }

    return render(request, 'admin_dashboard.html', context)









@staff_member_required(login_url='admin_login')
@never_cache
def report(request):
    interval = request.GET.get('interval', 'day')
    download = request.GET.get('download', None)

    now = timezone.now()
    if interval == 'month':
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
    elif interval == 'week':
        start_date = now - timedelta(days=now.weekday(), hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        end_date = start_date + timedelta(days=7) - timedelta(seconds=1)
    elif interval == 'year':
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date.replace(year=start_date.year + 1) - timedelta(seconds=1)
    else:  # day
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1) - timedelta(seconds=1)

    orders = Order.objects.filter(order_date__gte=start_date, order_date__lt=end_date)

    for order in orders:
        order.order_items = OrderItem.objects.filter(order=order)

    total_sales = orders.aggregate(total_sales=Sum('total_cost'))['total_sales'] or 0
    products_sold_count = OrderItem.objects.filter(order__in=orders).count()
    coupons_used_count = orders.exclude(coupon__isnull=True).count()

    if download:
        excel_data = generate_excel_data(orders, total_sales, products_sold_count, coupons_used_count)

        response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=sales_report.xlsx'
        return response

    context = {
        'total_sales': total_sales,
        'start_date': start_date,
        'end_date': end_date,
        'interval': interval.capitalize(),
        'orders': orders,
        'products_sold_count': products_sold_count,
        'coupons_used_count': coupons_used_count,
    }

    return render(request, 'sales_report.html', context)

def generate_excel_data(orders, total_sales, products_sold_count, coupons_used_count):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sales Report"

    ws.append(["Order ID", "Products Ordered", "Subtotal", "Coupon Discount", "Offer Applied", "Total Cost"])

    for order in orders:
        products_ordered = ", ".join([item.product.name for item in order.order_items])
        coupon_discount = order.coupon.discount_amount if order.coupon else "None"
        offer_applied = order.order_items.first().offer.description if order.order_items.first().offer else "None"
        ws.append([order.id, products_ordered, order.subtotal, coupon_discount, offer_applied, order.total_cost])

    ws.append([])
    ws.append(["Total Sales", total_sales])
    ws.append(["Products Sold Count", products_sold_count])
    ws.append(["Coupons Used Count", coupons_used_count])

    from io import BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return output






########admin products##################admin products######################admin products######################admin products###############admin products##########################

@staff_member_required(login_url='admin_login')
@never_cache
def admin_product(request):
    query = request.GET.get('query')
    products = Product.objects.all().order_by('id')
    
    if query:
        products = products.filter(name__icontains=query)  
        
    return render(request, 'admin_product.html', {'products': products,'query': query})






@staff_member_required(login_url='admin_login')
@never_cache
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_product') 
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})




@staff_member_required(login_url='admin_login')
@never_cache
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_product')  
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'edit_product.html', {'form': form})





@staff_member_required(login_url='admin_login')
@require_POST
def list_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_listed = True
    product.save()
    return redirect('admin_product')  



@staff_member_required(login_url='admin_login')
@require_POST
def unlist_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_listed = False
    product.save()
    return redirect('admin_product') 






















#####admin categories ##########################admin categories #########################admin categories #################admin categories #####################


@staff_member_required(login_url='admin_login')
@never_cache
def admin_categories(request):
    categories = Category.objects.all().order_by('id')

    
    return render(request, 'admin_categories.html',  {'categories': categories})





@staff_member_required(login_url='admin_login')
@never_cache
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')  
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})






@staff_member_required(login_url='admin_login')
@never_cache
def edit_category(request, category_id):  
    category = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')  
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form})







@staff_member_required(login_url='admin_login')
@require_POST
def list_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.is_listed = True
    category.save()
    return redirect('admin_categories')  



@staff_member_required(login_url='admin_login')
@require_POST
def unlist_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.is_listed = False
    category.save()
    return redirect('admin_categories') 











############admin users###################admin users##############admin users####################admin users##########################
@staff_member_required(login_url='admin_login')
def search_users(request):
    query = request.GET.get('query', '')
    users = CustomUser.objects.filter(username__icontains=query)
    
    return render(request, 'admin_users.html', {'users': users, 'query': query})






@staff_member_required(login_url='admin_login')
@never_cache
def block_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False
    user.save()
    return redirect('admin_users')




@staff_member_required(login_url='admin_login')
@never_cache
def unblock_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.save()
    return redirect('admin_users')




 
@staff_member_required(login_url='admin_login')
@never_cache
def admin_users(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        users = CustomUser.objects.filter(username__icontains=query, is_superuser=False).order_by('id')
    else:
        users = CustomUser.objects.filter(is_superuser=False)  
    
    
    return render(request, 'admin_users.html', {'users': users, 'query': query})
  









##################admin_orders###############admin_orders#################admin_orders############admin_orders############






@staff_member_required(login_url='admin_login')
@never_cache
def admin_orders(request):
    query = request.GET.get('query', '')
    orders = Order.objects.filter(user__username__icontains=query).order_by('-id')
    
    for order in orders:
        order.order_items = OrderItem.objects.filter(order=order)
        
        for item in order.order_items:
            item.product = item.product 

    return render(request, 'admin_orders.html', {'orders': orders, 'query': query})





@staff_member_required(login_url='admin_login')
@never_cache
def admin_order_items(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    order_items = OrderItem.objects.filter(order=order).order_by('id')
    for item in order_items:
        item.product = item.product  
        razorpay_order = order.razorpay_order
        is_paid = razorpay_order.paid if razorpay_order else False    

    return render(request, 'admin_order_items.html', {'order': order, 'order_items': order_items,'is_paid': is_paid})







@staff_member_required(login_url='admin_login')
def admin_change_order_status(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(item.ORDER_STATUS_CHOICES):
            if new_status == 'Cancelled' and item.status != 'Cancelled':
                item.status = 'Cancelled'
                item.save()
                
                if item.order.payment_method.lower() == 'razorpay':
                    try:
                        user_wallet, created = Wallet.objects.get_or_create(user=item.order.user)
                        user_wallet.balance += item.total_price
                        user_wallet.save()
                        
                        Transaction.objects.create(
                            user=item.order.user,
                            amount=item.total_price,
                            transaction_type='Refund',
                            order=item.order
                        )
                    except Exception as e:
                        messages.error(request, f'Error processing refund: {e}')
                
            else:
                item.status = new_status
                item.save()
                
            messages.success(request, 'Order item status updated successfully.')
        else:
            messages.error(request, 'Invalid order item status.')
    
    return redirect('admin_order_items', order_id=item.order.id)





#########cancellation request##########cancellation request###########cancellation request#############cancellation request############cancellation request##



@staff_member_required(login_url='admin_login')
def review_cancellation_requests(request):
    requests = CancellationRequest.objects.filter().order_by('-id')
    return render(request, 'cancellation_request.html', {'requests': requests})


@staff_member_required(login_url='admin_login')
def approve_cancellation_request(request, request_id):
    cancellation_request = get_object_or_404(CancellationRequest, id=request_id)
    if not cancellation_request.is_approved:
        cancellation_request.is_approved = True
        cancellation_request.reviewed_at = timezone.now()
        cancellation_request.save()
        
        order_item = cancellation_request.order_item
        if order_item.status != 'Cancelled':
            order_item.status = 'Cancelled'
            order_item.save()
            
            if order_item.order.payment_method.lower() == 'razorpay':
                try:
                    user_wallet, created = Wallet.objects.get_or_create(user=order_item.order.user)
                    user_wallet.balance += order_item.total_price
                    user_wallet.save()
                    Transaction.objects.create(
                        user=order_item.order.user,
                        amount=order_item.total_price,
                        transaction_type='Refund',
                        order_id=order_item.order.id
                    )
                except Wallet.DoesNotExist:
                    pass
        
    return redirect('review_cancellation_requests')


########admin coupon############admin coupon###################admin coupon##############admin coupon############admin coupon#################################################################





@staff_member_required(login_url='admin_login')
def admin_coupons(request):
    coupons = Coupon.objects.all().order_by('id')
    return render(request, 'admin_coupons.html', {'coupons': coupons})






def generate_coupon_code(length=10):
    """Generate a random alphanumeric coupon code."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))



def add_coupon(request):
    generated_code = generate_coupon_code()
    initial_data = {
        'code': generated_code,
        'valid_from': timezone.now(),
    }

    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_coupons')
    else:
        form = CouponForm(initial=initial_data)
    
    return render(request, 'add_coupon.html', {'form': form, 'generated_code': generated_code})



@staff_member_required(login_url='admin_login')
def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('admin_coupons')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'edit_coupon.html', {'form': form})








@staff_member_required(login_url='admin_login')
def delete_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    if request.method == 'POST':
        coupon.delete()
        return redirect('admin_coupons')
    return render(request, 'delete_coupon.html', {'coupon': coupon})












###########admin offers###########admin offers#################admin offers############admin offers###########admin offers###########################################



@staff_member_required(login_url='admin_login')
def admin_offers(request):
    offers = Offer.objects.all().order_by('id')
    return render(request, 'admin_offers.html', {'offers': offers})





@staff_member_required(login_url='admin_login')
def add_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_offers')
    else:
        form = OfferForm()
    return render(request, 'add_offer.html', {'form': form})





@staff_member_required(login_url='admin_login')
def edit_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('admin_offers')
    else:
        form = OfferForm(instance=offer)
    return render(request, 'edit_offer.html', {'form': form})





@staff_member_required(login_url='admin_login')
def delete_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    offer.delete()
    return redirect('admin_offers')










##########sales report##########sales report########sales report##########sales report##########sales report##############sales report######sales report#######





def sales_report(request):
   
    return render(request, 'sales_report.html')
















###########admin login ######################admin login ###################admin login ############################################



@never_cache  
def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
             return redirect('admin_dashboard')
        else:
            pass
    form = AuthenticationForm(request, request.POST or None)

    if request.method == "POST":
        username = request.POST.get('username') 
        password = request.POST.get('password') 
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            request.session['username'] = username
            return redirect('admin_dashboard')
            
    
    else:
        form = AuthenticationForm()
    
    return render(request, 'admin_login.html', {'form': form}) 
  


@staff_member_required(login_url='admin_login')
@never_cache
def logout_admin(request):
    logout(request)
    request.session.flush()
    return render(request, 'after_admin_logout.html')




