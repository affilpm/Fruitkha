from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.utils import timezone




class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15)
    
    
    
class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)  
    name = models.CharField(max_length=100)  

    def __str__(self):
        return f"{self.name}: {self.street}, {self.city}, {self.state}, {self.country}"


    
    
    
    
    
    
    






class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    is_listed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Offer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
    


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='products/', blank=True, null=True)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    is_listed = models.BooleanField(default=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_offer')
    related_products = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_to')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        current_date = timezone.now().date()

        if self.offer and self.offer.start_date <= current_date <= self.offer.end_date:
            if not self.original_price:
                self.original_price = self.price
            self.price = self.original_price - (self.original_price * self.offer.discount_percentage / 100)
        else:
            if self.original_price:
                self.price = self.original_price
                self.original_price = None

        super(Product, self).save(*args, **kwargs)

        if self.image1:
            img = Image.open(self.image1.path)
            fixed_size = (300, 300)
            img.thumbnail(fixed_size)
            img.save(self.image1.path)

        if self.image2:
            img = Image.open(self.image2.path)
            fixed_size = (300, 300)
            img.thumbnail(fixed_size)
            img.save(self.image2.path)

        # Resize and save the third image
        if self.image3:
            img = Image.open(self.image3.path)
            fixed_size = (300, 300)
            img.thumbnail(fixed_size)
            img.save(self.image3.path)




class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name