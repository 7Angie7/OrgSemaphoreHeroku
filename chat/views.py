from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def control(request):
    return render(request, 'control.html', {})


def mainpage(request):
    return render(request, 'mainpage.html', {})


def dashboard(request):
    return render(request, 'dashboard.html', {})


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

