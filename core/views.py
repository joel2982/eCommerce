from django.shortcuts import render, redirect, get_object_or_404
from core.forms import *
from django.contrib import messages
from django.utils import timezone

# Create your views here.
def index(request):    
    products = Product.objects.all()
    return render(request, 'core/index.html',{"products":products})

def cart(request):
    order = Order.objects.filter(user=request.user, ordered=False).first()
    if order :
        print(order)
        return render(request, 'core/cart.html',{"order":order})
    
    return render(request, 'core/cart.html',{"Message":'Your Cart is Empty.'})

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
    # save the page we came from
    current_page = request.META.get('HTTP_REFERER')
    # get the product
    product = Product.objects.get(pk=pk)
    # create order item
    order_item, created = Order_Item.objects.get_or_create(
        product=product,
        user = request.user,
        )
    print(order_item, current_page)
    # get queryset of the Order object of the particular User
    current_order = Order.objects.filter(user=request.user, ordered = False).first()
    if current_order:
        if order_item.quantity >= product.product_count:
            messages.info(request,f'Limited Stock Available for {product.name}')
        elif current_order.order_items.filter(product__pk=pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,f"{product.name}'s quantity in your Cart has been Updated.")
        else:
            current_order.order_items.add(order_item)
            messages.info(request,'Item added to Cart')
    else:
        order_date = timezone.now()
        order = Order.objects.create(user=request.user, order_date=order_date)
        order.order_items.add(order_item)
    return redirect(current_page,pk=pk)


def remove_from_cart(request,pk):
    product = get_object_or_404(Product,pk=pk)
    current_page = request.META.get('HTTP_REFERER')
    current_order = Order.objects.filter(user=request.user, ordered = False).first()
    if not current_order:
        messages.info(request, f"{product.name} is not in the Cart.")
    elif current_order.order_items.filter(product__pk=pk).exists():
        order_item = Order_Item.objects.filter(product=product,user = request.user).first()
        if order_item.quantity <= 1:
            order_item.delete()
            messages.info(request,f"{product.name} has been removed from the Cart.")
        else:
            order_item.quantity -= 1
            order_item.save()
            messages.info(request,f"{product.name}'s quantity in your Cart has been Updated.")
    else:
        messages.info(request, f"{product.name} is not in the Cart.")
    return redirect(current_page,pk=pk)
