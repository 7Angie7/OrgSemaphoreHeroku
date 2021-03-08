from django.urls import path
from . import views


urlpatterns = [
    path('', views.empty, name='empty'),
    path('control/', views.control, name='control'),
    path('mainpage/', views.mainpage, name='mainpage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('semaphore/', views.semaphore, name='semaphore'),
    path('logoutUser/', views.logoutUser, name='logoutUser'),
]