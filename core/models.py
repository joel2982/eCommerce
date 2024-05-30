from typing import Iterable
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
    

class Order_Item(models.Model):
    product = models.ForeignKey(Product,null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self) -> str:
        return f'{self.quantity} of {self.product.name}'
    def get_order_item_price(self) -> float:
        return self.quantity*self.product.price

class Order(models.Model):
    order_items = models.ManyToManyField(Order_Item)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(default=0.0)
    ordered = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, blank=True, null=True, unique=True, default=None)
    order_date = models.DateTimeField()
    # shipment related attributes 
    order_delivered = models.BooleanField(default=False)
    order_received = models.BooleanField(default=False)
    # payment related attributes
    datetime_payment = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    def save(self ,*args ,**kwargs):
        if self.order_id is None and self.id and self.datetime_payment:
            self.order_id = self.datetime_payment.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        # updating and saving the value to the table
        return super().save(*args ,**kwargs)
    
    def __str__(self) -> str:
        if self.order_id:
            return self.order_id
        return self.user.username
    
    def get_total_price(self) -> float:
        total = 0.0
        for order_item in self.order_items.all():
            total += order_item.get_order_item_price()
        return total
    
    def get_total_count(self) -> int:
        order = Order.objects.get(pk=self.pk)
        return order.order_items.count()
    
