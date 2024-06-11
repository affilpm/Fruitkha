from django.urls import path
from . import views


urlpatterns = [
  
    path('checkout/', views.checkout, name='checkout'),
    path('add_address_checkout/', views.add_address_checkout, name='add_address_checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_success/', views.order_success, name='order_success'),
    
    path('orders/', views.orders, name='orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('retry_razorpay/', views.retry_razorpay, name="retry_razorpay"),
    path('request_item_cancellation/<int:item_id>/', views.request_item_cancellation, name='request_item_cancellation'),
    
    path('order_invoice/<int:order_id>/', views.generate_invoice, name='order_invoice'),
    
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove_coupon/', views.remove_coupon, name='remove_coupon'),
    
    
    
    path('wallet/', views.wallet, name='wallet'),
    path('save_order/', views.save_order, name='save_order'),
    
    
    path('razorpay/', views.razorpay_view, name='razorpay'),
    path('payment_success/', views.success, name='payment_success'),
    
    
]
