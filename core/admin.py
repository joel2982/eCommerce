from django.contrib import admin
from core.models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order_Item)
admin.site.register(Order)