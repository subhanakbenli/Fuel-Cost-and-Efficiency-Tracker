from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("index", views.index_view, name="index"),
    path("about", views.about_view, name="about"),
    path("add_data", views.add_data, name="add_data"),
    path("login/", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path('password/', views.password, name='password'),
    path("logout/", views.logout_view, name="logout"),
    
    path("tables", views.show_tables, name="show_tables"),
    path("charts/", views.show_charts, name="show_charts"),
    path('get_charts/', views.get_charts, name='get_charts'),
]
