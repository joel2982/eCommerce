from django.shortcuts import render, redirect
from core.forms import *
from django.contrib import messages
from django.utils import timezone

# Create your views here.
def index(request):    
    products = Product.objects.all()
    return render(request, 'core/index.html',{"products":products})

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Product Added Successfully!")
            return redirect("/")
        else:
            messages.info(request,"Product is not Added, Try Again")
    else:
        form = ProductForm()
    return render(request, "core/add_product.html", {"form": form})

def product_desc(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request,'core/product_desc.html', {"product":product})

def add_to_cart(request, pk):
    # get the product
    product = Product.objects.get(pk=pk)
    # create order item
    order_item, created = Order_Item.objects.get_or_create(
        product=product,
        user = request.user,
        )
    print(order_item)
    # get queryset of the Order object of the particular User
    current_order = Order.objects.filter(user=request.user, ordered = False).first()
    if current_order:
        if current_order.order_items.filter(product__pk=pk).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            current_order.order_items.add(order_item)
    else:
        order_date = timezone.now()
        order = Order.objects.create(user=request.user, order_date=order_date)
        order.order_items.add(order_item)
    messages.info(request,'Item added to Cart')
    return redirect('product_desc',pk=pk)
