from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


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


def semaphore(request):
    return render(request, 'semaphore.html', {})


def logoutUser(request):
    logout(request)
    return redirect('mainpage')


def addSemaphore(request):
    return render(request, 'addSemaphore.html', {})


def contact(request):
    return render(request, 'contact.html', {})
