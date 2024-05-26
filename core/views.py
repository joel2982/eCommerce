from django.shortcuts import render, redirect
from core.forms import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

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




#     if request.method == 'POST':
#         form = ProductForm(request.POST,request.FILES)
#         if form.is_valid():
#             print('valid')
#             form.save()
#             print("Data Saved Successfully")
#             messages.success(request, "Product Added Successfully")
#             return redirect("/")
#         else:
#             print("Not Working")
#             messages.info(request,"Product is not Added, Try Again")
#     else:
#         form = ProductForm()
#     return render(request, 'core/add_product.html', {'form':form})