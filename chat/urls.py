from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('control/', views.control, name='control'),
    path('mainpage/', views.mainpage, name='mainpage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
]