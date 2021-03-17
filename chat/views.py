from django.shortcuts import render, redirect
from .models import *
from .forms import CreateUserForm, AddSemaphoreForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def empty(request):
    return redirect('mainpage')


def control(request):
    return render(request, 'control.html', {})


def mainpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, "Username OR password is incorrect")

    return render(request, 'mainpage.html', {})


@login_required(login_url='mainpage')
def dashboard(request):
    semaphores = Semaphore.objects.all()
    return render(request, 'dashboard.html', {'semaphores':semaphores})


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, user + ", your account was created. Please, log in.")
            return redirect('mainpage')

    context = {'form': form}
    return render(request, 'register.html', context)


@login_required(login_url='mainpage')
def semaphore(request):
    return render(request, 'semaphore.html', {})


def logoutUser(request):
    logout(request)
    return redirect('mainpage')


@login_required(login_url='mainpage')
def addSemaphore(request):
    form = AddSemaphoreForm()

    if request.method == 'POST':
        form = AddSemaphoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'addSemaphore.html', context)


def contact(request):
    return render(request, 'contact.html', {})
