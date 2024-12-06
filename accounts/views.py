from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseForbidden


# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username,password=password)
                user.save()
                print(user)
                messages.success(request,"Account created succefully")

                return redirect('ConstructTech:index')
            except:
                messages.error(request,"username already exist")

        else:
            messages.error(request,"password do not match")

    return render(request,'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('ConstructTech:index')  # Adjust as necessary
        else:
            messages.error(request, "Invalid username or password")
            return redirect('accounts:login')

    return render(request, 'accounts/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')  # Redirect to login page
    else:
        return HttpResponseForbidden("Forbidden: This URL only accepts POST requests.")


    