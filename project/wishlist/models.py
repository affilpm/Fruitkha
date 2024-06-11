from django.db import models
from home.models import CustomUser, Product
# Create your models here.



class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # class Meta:
    #     unique_together = ('user', 'product')
    # Add other fields as needed