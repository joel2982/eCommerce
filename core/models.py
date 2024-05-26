from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    # extra fields
    phone_no = models.CharField(max_length=12, blank=False, verbose_name='phone number with country code')

    def __str__(self) -> str:
        return self.user.username
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name
    

class Product(models.Model):
    name = models.CharField(null=False, blank=False, max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField(default=0.0)
    product_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/')

    def __str__(self) -> str:
        return self.name