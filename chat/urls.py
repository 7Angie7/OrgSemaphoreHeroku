from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admin_page/', views.admin_page, name='admin_page'),
]