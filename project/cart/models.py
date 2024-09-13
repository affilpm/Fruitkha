from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from home.models import Product, CustomUser, Category 

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')
        
