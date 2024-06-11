from django.contrib import admin
from .models import Order, Coupon, OrderItem, Wallet, Razorpay_Order, CancellationRequest, Transaction ,Order_Address



admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(OrderItem)
admin.site.register(Wallet)
admin.site.register(Razorpay_Order)
admin.site.register(CancellationRequest)
admin.site.register(Transaction)
admin.site.register(Order_Address)




