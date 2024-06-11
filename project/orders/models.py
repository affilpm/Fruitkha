from django.db import models
from home.models import CustomUser, Product, Offer
from django.utils import timezone




class Order_Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.street}, {self.city}, {self.country}"


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey('Coupon' , on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey(Order_Address, on_delete=models.SET_NULL, null=True, blank=True)
    PAYMENT_CHOICES = (
        ('cash_on_delivery', 'Cash on Delivery'),
        ('razorpay', 'razorpay'),
    )
    payment_method = models.CharField(max_length=100, choices=PAYMENT_CHOICES)
    order_date = models.DateTimeField(auto_now_add=True)
    total_products = models.PositiveIntegerField(default=0)
    original_total = models.DecimalField(max_digits=10, decimal_places=2)  
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order = models.OneToOneField('Razorpay_Order', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"Order #{self.pk}"  
   

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer , on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField(default=1)
    original_price_total = models.DecimalField(max_digits=10, decimal_places=2) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2) 
    offer = models.ForeignKey(Offer , on_delete=models.SET_NULL, null=True, blank=True)
    
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
    ]
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending', null=True)

    def __str__(self):
        return f"OrderItem #{self.pk} in Order #{self.order.pk}" 
   

class CancellationRequest(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reason = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    reviewed_at = models.DateTimeField(null=True, blank=True)



class Razorpay_Order(models.Model):
    paid = models.BooleanField(default=False)
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)







    
class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20) 
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    
    
    
    
class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)    
    
    def __str__(self):
        return f"Wallet for {self.user.username}"




class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_required = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def is_user_eligible(self, user):
        return self.is_active and self.valid_from <= timezone.now() <= self.valid_to and not Coupon.objects.filter(user=user).exists()

 


