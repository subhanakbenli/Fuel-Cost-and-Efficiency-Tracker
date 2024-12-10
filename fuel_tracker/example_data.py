from django.contrib.auth.models import User
from pages.models import Car, Fuel
from datetime import date

# Kullanıcı oluştur (Eğer yoksa)
user, created = User.objects.get_or_create(username="test_user", defaults={"email": "test@example.com"})
if created:
    user.set_password("securepassword123")  # Kullanıcıya şifre ata
    user.save()
# Araç oluştur
car = Car.objects.create(
    car_name="Tesla Model S",
    car_brand="Tesla",
    car_model="Model S",
    car_volume=2.0,
    created_by=user
)

# Yakıt girişleri oluştur
fuel_1 = Fuel.objects.create(
    car=car,
    fuel_date=date(2024, 12, 1),
    fuel_firm="Petrol Ofisi",
    fuel_volume=50.0,
    fuel_cost=1000.0,
    car_km=10000.0
)

fuel_2 = Fuel.objects.create(
    car=car,
    fuel_date=date(2024, 12, 5),
    fuel_firm="Shell",
    fuel_volume=40.0,
    fuel_cost=800.0,
    car_km=10200.0
)

print(f"Created car: {car}")
print(f"Created fuel entries: {fuel_1}, {fuel_2}")





# Kullanıcı oluştur (Eğer yoksa)
user, created = User.objects.get_or_create(username="test_user", defaults={"email": "test@example.com"})

if created:
    user.set_password("securepassword123")  # Kullanıcıya şifre ata
    user.save()

print(f"User created: {user.username}, Password: securepassword123")