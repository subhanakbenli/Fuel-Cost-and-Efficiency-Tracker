from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from datetime import date
from .models import Fuel,Car

from datetime import date, timedelta
from django.shortcuts import render
from django.db.models import Sum

def index_view(request):
    user, created = User.objects.get_or_create(username="test_user", defaults={"email": "test@example.com"})

    login(request, user)
    # Bugünün tarihi
    today_date = date.today().strftime('%Y-%m-%d')

    # Kullanıcıya ait araçları filtrele
    vehicles = Car.objects.filter(created_by=request.user)

    monthly_labels, monthly_cost,monthly_volume, daily_labels, daily_data = get_charts_data(request, selected_vehicle=vehicles.first())
        
    # Yakıt verilerini al
    fuel_data = Fuel.objects.filter(car__in=vehicles).values(
    'car__car_name',  # Car modelinden car_name alanı
    'fuel_firm',      # Fuel modelindeki fuel_firm alanı
    'fuel_type',      # Fuel modelindeki fuel_type alanı
    'fuel_volume',    # Fuel modelindeki fuel_volume alanı
    'fuel_cost',      # Fuel modelindeki fuel_cost alanı
    'car_km',         # Fuel modelindeki car_km alanı
    'fuel_date'       # Fuel modelindeki fuel_date alanı
)

    # Sabit firma listesi
    firms = ["Shell", "BP", "Opet", "Total"]
    # Context verisi
    context = {   
        'today_date': today_date,
        'vehicles': vehicles,
        'selected_vehicle': vehicles.first(),
        'fuel_types': ["Benzin", "Dizel", "LPG"],
        'selected_fuel_type': "Benzin",
        'firms': firms,        
        'bar_labels': monthly_labels, 
        'bar_data': monthly_volume,     
        'area_labels': daily_labels,
        'area_data': daily_data,
        'montly_area_labels': monthly_labels,
        'montly_area_data': monthly_cost,
        'fuel_data': fuel_data,
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
        fuel_type = request.POST['fuel_type']
        fuel_volume = request.POST['fuel_amount']
        total_cost = request.POST['total_cost']
        firm = request.POST['firm_name']
        car_km = request.POST['car_km']
        
        if vehicle =='other':
            vehicle = request.POST['custom_vehicle_name']
        
        related_car = Car.objects.filter(created_by=request.user,
                                     car_name=vehicle).first()
        if not related_car:
            related_car = Car.objects.create(created_by=request.user,
                                         car_name=vehicle)
            related_car.save()
        fuel = Fuel.objects.create(car=related_car, 
                            fuel_date=fuel_date,
                            fuel_type=fuel_type, 
                            fuel_volume=fuel_volume, 
                            fuel_cost=total_cost, 
                            fuel_firm=firm, 
                            car_km=car_km)
        fuel.save()
        # Veritabanına kaydet
        # Örnek: Fuel.objects.create(vehicle=vehicle, fuel_type=fuel_type, fuel_amount=fuel_amount, fuel_price=fuel_price, firm=firm, date=date)
        messages.success(request, "Data added successfully!")
        return redirect('index')

    
    return redirect('index')

@login_required
def show_tables(request):
    return render(request, "tables.html")

@login_required
def get_charts_data(request, selected_vehicle=None,selected_fuel_type=None):
    vehicles = Car.objects.filter(created_by=request.user)
    current_year = date.today().year

    monthly_fuel_data = Fuel.objects.filter(
        car=selected_vehicle,  # Belirli bir araç seçiliyor
        fuel_type=selected_fuel_type,  # Belirli bir yakıt tipi seçiliyor
        fuel_date__year=current_year  # Yıl filtresi uygulanıyor
    ).values_list('fuel_date__month').annotate(
        total_volume=Sum('fuel_volume'),  # Aynı aya ait yakıt hacimleri toplanıyor
        total_cost=Sum('fuel_cost')
    ).order_by('fuel_date__month')  # Aylara göre sıralama yapılıyor
        
    
    # Bar ve Area Chart için verileri hazırla
    monthly_labels = [
        "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
        "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    monthly_cost = [0] * 12
    monthly_volume = [0] * 12
    for month, total_volume,total_cost in monthly_fuel_data:
        monthly_cost[month - 1] = total_cost
        monthly_volume[month - 1] = total_volume

    # Son 13 gün için yakıt tüketimi (Area Chart için)
    start_date = date.today() - timedelta(days=12)
    daily_fuel_data = Fuel.objects.filter(
        car__in=vehicles,
        fuel_type=selected_fuel_type,
        fuel_date__gte=start_date
        
    ).order_by('fuel_date')

    daily_labels = [entry.fuel_date.strftime("%b %d") for entry in daily_fuel_data]
    daily_data = [entry.fuel_volume for entry in daily_fuel_data]
    if len(daily_labels)==0:
        daily_labels = ["No Data"]
        daily_data = [0]
    for i in daily_data:
        print(i)
    
    return monthly_labels, monthly_cost, monthly_volume, daily_labels, daily_data

def show_charts(request):
    
    # Kullanıcıya ait araçları filtrele
    vehicles = Car.objects.filter(created_by=request.user)

    # Aylık yakıt tüketimi (Bar ve Area Chart için)
    monthly_labels, monthly_cost,monthly_volume, daily_labels, daily_data = get_charts_data(request, selected_vehicle=vehicles.first())

    context = {
        'bar_labels': monthly_labels,
        'bar_data': monthly_volume,  
        'area_labels': daily_labels,
        'area_data': daily_data,
        'montly_area_labels': monthly_labels,
        'montly_area_data': monthly_cost
    }
    return render(request, 'charts.html', context)


from django.http import JsonResponse

def get_charts(request):
    vehicle = request.GET.get('vehicle')
    fuel_type = request.GET.get('fuel')
    print(vehicle, fuel_type)
    # Verileri filtreleyin
    # Örneğin:
    # monthly_labels, monthly_cost, daily_labels, daily_data = get_charts_data(request, selected_vehicle=vehicle, selected_fuel_type=fuel_type)
    related_car = Car.objects.filter(created_by=request.user,car_name=vehicle).first()
    monthly_labels, monthly_cost,monthly_volume, daily_labels, daily_data = get_charts_data(request, selected_vehicle=related_car, selected_fuel_type=fuel_type)
    return JsonResponse({
        'bar_labels': monthly_labels, 
        'bar_data': monthly_volume,     
        'area_labels': daily_labels,
        'area_data': daily_data,
        'montly_area_labels': monthly_labels,
        'montly_area_data': monthly_cost,
    })

