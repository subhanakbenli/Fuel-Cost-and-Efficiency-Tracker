from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("about", views.about, name="about"),
    
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password/', views.password_reset_view, name='password'),
    path("logout", views.logout, name="logout"),
    path("tables", views.show_tables, name="show_tables"),
    path("charts/", views.show_charts, name="show_charts"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("layout_static", views.layout_static, name="layout_static"),
    path("layout_sidenav", views.layout_sidenav, name="layout_sidenav"),
]
