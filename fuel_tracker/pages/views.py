from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from datetime import date
from .models import Fuel
def index(request):
    today_date = date.today().strftime('%Y-%m-%d')
    # vehicles
    vehicles = ["Car", "Motorcycle", "Truck", "Bus", "Bicycle"]
    # montly fuel consumption
    montly_area_labels = ["January", "February", "March", "April", "May", "June"]
    montly_area_data = [4215, 5312, 6251, 7841, 9821, 14984]
    # Bar Chart Verileri
    bar_labels = ["January", "February", "March", "April", "May", "June"]
    bar_data = [4215, 5312, 6251, 7841, 9821, 14984]

    # Area Chart Verileri
    area_labels = ["Mar 1", "Mar 2", "Mar 3", "Mar 4", "Mar 5", "Mar 6", "Mar 7", "Mar 8", "Mar 9", "Mar 10", "Mar 11", "Mar 12", "Mar 13"]
    area_data = [10000, 30162, 26263, 18394, 18287, 28682, 31274, 33259, 25849, 24159, 32651, 31984, 38451]

    # Context ile template'e gönder
    firms = ["Shell", "BP", "Opet", "Total"]  # Dinamik liste olabilir (ör. veri tabanından çekilebilir)
    context = {
        'today_date': today_date,
        'vehicles': vehicles,
        'bar_labels': bar_labels,
        'bar_data': bar_data,
        'area_labels': area_labels,
        'area_data': area_data,
        'montly_area_labels': montly_area_labels,
        'montly_area_data': montly_area_data,
        'firms': firms
    }
    return render(request, 'index.html', context)

def about_view(request):
    return render(request, "about.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Kullanıcıyı doğrula
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)  # Giriş yap
            messages.success(request, "Login successful!")
            return redirect("index")  # Giriş sonrası yönlendirilecek sayfa
        else:
            # Hatalı giriş durumunda mesaj göster
            messages.error(request, "Invalid email or password.")
    
    # GET isteği için login template'ini render et
    return render(request, "login.html")

def register_view(request):
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

@login_required
def logout_view(request):
    logout(request)  # Kullanıcıyı çıkış yap
    return redirect('index')  # 'index' URL adınıza yönlendir

def password(request):
    return render(request, "password.html")


def add_data(request):
    if request.method == 'POST':
        vehicle = request.POST['vehicle_name']
        fuel_date = request.POST['fuel_date']
        fuel_volume = request.POST['fuel_amount']
        total_cost = request.POST['total_cost']
        firm = request.POST['firm_name']
        car_km = request.POST['car_km']
        print(vehicle, fuel_date ,fuel_volume,total_cost,firm )
        Fuel.objects.create(car=vehicle, 
                            fuel_date=fuel_date, 
                            fuel_volume=fuel_volume, 
                            fuel_cost=total_cost, 
                            fuel_firm=firm, 
                            car_km=car_km)
        # Veritabanına kaydet
        # Örnek: Fuel.objects.create(vehicle=vehicle, fuel_type=fuel_type, fuel_amount=fuel_amount, fuel_price=fuel_price, firm=firm, date=date)
        messages.success(request, "Data added successfully!")
        return redirect('index')

    
    return redirect('index')

@login_required
def show_tables(request):
    return render(request, "tables.html")
# @login_required


def show_charts(request):
    
     # montly fuel consumption
    montly_area_labels = ["January", "February", "March", "April", "May", "June"]
    montly_area_data = [4215, 5312, 6251, 7841, 9821, 14984]
    # Bar Chart Verileri
    bar_labels = ["January", "February", "March", "April", "May", "June"]
    bar_data = [4215, 5312, 6251, 7841, 9821, 14984]

    # Area Chart Verileri
    area_labels = ["Mar 1", "Mar 2", "Mar 3", "Mar 4", "Mar 5", "Mar 6", "Mar 7", "Mar 8", "Mar 9", "Mar 10", "Mar 11", "Mar 12", "Mar 13"]
    area_data = [10000, 30162, 26263, 18394, 18287, 28682, 31274, 33259, 25849, 24159, 32651, 31984, 38451]

    # Context ile template'e gönder
    context = {
        'montly_area_labels': montly_area_labels,
        'montly_area_data': montly_area_data,
        'bar_labels': bar_labels,
        'bar_data': bar_data,
        'area_labels': area_labels,
        'area_data': area_data,
    }
    return render(request, 'charts.html', context)



