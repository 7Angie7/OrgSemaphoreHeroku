from django.urls import path
from . import views


urlpatterns = [
    path('', views.empty, name='empty'),
    path('mainpage/', views.mainpage, name='mainpage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('semaphore/<str:pk_test>', views.semaphore, name='semaphore'),
    path('logoutUser/', views.logoutUser, name='logoutUser'),
    path('addSemaphore/', views.addSemaphore, name='addSemaphore'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contact/', views.contact, name='contact'),
    path('control/<str:pk_test>/', views.control, name='control'),
    path('control/<str:pk_test>/deleteSemap/', views.deleteSemap, name='deleteSemap'),
    path('dashboard/deleteAccount/', views.deleteAccount, name='deleteAccount'),
    path('dashboard/editAccount/', views.editAccount, name='editAccount'),
    path('readyAlertUrl/<str:pk_test>/', views.readyAlertUrl, name='readyAlertUrl'),
    path('busyAlertUrl/<str:pk_test>/', views.busyAlertUrl, name='busyAlertUrl'),
    path('joinQueueUrl/<str:pk_test>/<str:client_name>/', views.joinQueueUrl, name='joinQueueUrl'),
    path('checkQueueUrl/<str:pk_test>/', views.checkQueueUrl, name='checkQueueUrl'),
    path('helloQueueUrl/<str:pk_test>/', views.helloQueueUrl, name='helloQueueUrl'),
    path('manageSemUrl/<str:pk_test>/', views.manageSemUrl, name='manageSemUrl'),
    path('editLastClient/<str:pk_test>/', views.editLastClient, name='editLastClient'),
    path('editClientInfo/<str:pk_test>/', views.editClientInfo, name='editClientInfo'),
    path('checkEmptyQueue/<str:pk_test>/', views.checkEmptyQueue, name='checkEmptyQueue'),
    path('deleteClient/<str:pk_test>/', views.deleteClient, name='deleteClient'),
    path('cleanQueue/<str:pk_test>/', views.cleanQueue, name='cleanQueue'),
]