from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")


def login(request):
    return render(request, "login.html")

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        try:
            user = User.objects.create_user(
                username=email, 
                email=email, 
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
        except:
            messages.error(request, "Error creating account. Try again!")
            return redirect('register')

    return render(request, 'register.html')

def logout(request):
    return render(request, "logout.html")


def password(request):
    return render(request, "password.html")

def password_reset_view(request):
    return render(request, "password.html")

def dashboard(request):
    return render(request, "dashboard.html")

def show_tables(request):
    return render(request, "tables.html")

def show_charts(request):
    return render(request, "charts.html")

def layout_static(request):
    return render(request, "layout-static.html")

def layout_sidenav(request):
    return render(request, "layout-sidenav-light.html")

