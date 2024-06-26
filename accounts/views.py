from django.shortcuts import render,redirect
from core.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        current_user = authenticate(username=username, password=password)
        if current_user:
            login(request,current_user)
            return redirect('/')
        else:
            messages.info(request,'Username or Password Incorrect.')
            return redirect('user_login')
    return render(request, 'accounts/login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone_no = request.POST.get('phone_no')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(username,phone_no,email,password,confirm_password)
        if password != confirm_password :
            messages.info(request, 'Entered passwords do not match.')
            return redirect('user_register')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists.')
            return redirect('user_register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists.')
            return redirect('user_register')
        else:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            customer = Customer.objects.create(user=user, phone_no=phone_no)
            customer.save()
            # code for Immediate Login
            current_user = authenticate(username=username, password=password)
            if current_user:
                login(request,current_user)
                return redirect('/')
    return render(request, 'accounts/register.html')

def user_logout(request):
    logout(request)
    return redirect('/')