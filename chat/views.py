from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import CreateUserForm, AddSemaphoreForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def empty(request):
    return redirect('mainpage')


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
    user = request.user
    usersemap = semaphores.filter(author__username=user)
    return render(request, 'dashboard.html', {'usersemap': usersemap})


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




def logoutUser(request):
    logout(request)
    return redirect('mainpage')


@login_required(login_url='mainpage')
def addSemaphore(request):
    form = AddSemaphoreForm()

    if request.method == 'POST':
        form = AddSemaphoreForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.status = 'Busy'
            task.controlUrl = uuid.uuid4()
            task.queueNum = 0

            task.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'addSemaphore.html', context)


def contact(request):
    return render(request, 'contact.html', {})


@login_required(login_url='mainpage')
def control(request, pk_test):
    semap = Semaphore.objects.get(controlUrl=pk_test)
    semapClients = QueueClient.objects.filter(semap=semap, queueNum__gt=2)

    return render(request, 'control.html', {'semap': semap, 'pk_test': pk_test, 'semapClients': semapClients})


def semaphore(request, pk_test):
    semap = Semaphore.objects.get(controlUrl=pk_test)
    numQueueClients = QueueClient.objects.filter(semap=semap).count()

    return render(request, 'semaphore.html', {'semap': semap, 'pk_test': pk_test, 'numQueueClients': numQueueClients})


@login_required(login_url='mainpage')
def deleteSemap(request, pk_test):
    semap = Semaphore.objects.get(controlUrl=pk_test)

    if request.method == 'POST':
        semap.delete()
        return redirect('dashboard')

    return render(request, 'deleteSemap.html', {'semap': semap, 'pk_test': pk_test})


@login_required(login_url='mainpage')
def deleteAccount(request):
    user = request.user

    if request.method == 'POST':
        user.delete()
        return redirect('mainpage')

    return render(request, 'deleteAccount.html', {'user': user})


@login_required(login_url='mainpage')
def editAccount(request):
    user = request.user
    form = CreateUserForm(instance=user)

    if request.method == 'POST':
        form = CreateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'editAccount.html', context)


@csrf_exempt
def readyAlertUrl(request, pk_test):
    semap = Semaphore.objects.get(controlUrl=pk_test)
    semap.status = 'Ready'
    semap.save()
    return HttpResponse('Status changed to --Ready--')


@csrf_exempt
def busyAlertUrl(request, pk_test):
    semap = Semaphore.objects.get(controlUrl=pk_test)
    semap.status = 'Busy'
    semap.save()
    return HttpResponse('Status changed to --Busy--')


@csrf_exempt
def joinQueueUrl(request, pk_test):
    device = request.COOKIES['device']
    semap = Semaphore.objects.get(controlUrl=pk_test)
    lastClient = QueueClient.objects.last()

    # try get the last client in database
    if lastClient == None:
        firstclient, created = QueueClient.objects.get_or_create(device=device, semap=semap, queueNum=1)
        response = {
            'msg': "Change number of queue"
        }
        return JsonResponse(response)

    else:
        lastClientNumber = lastClient.queueNum
        newLastClientNumber = lastClientNumber + 1

    #check if the client is in DB
    try:
        client = QueueClient.objects.get(device=device, semap=semap)
        response = {
            'msg': "You are already in the queue"
        }
    except:
        client, created = QueueClient.objects.get_or_create(device=device, semap=semap, queueNum=newLastClientNumber)
        response = {
            'msg': "Change number of queue"
        }

    return JsonResponse(response)

@csrf_exempt
def resetQueueUrl(request, pk_test):
    semap = Semaphore.objects.get(controlUrl=pk_test)
    semap.queueNum = 0
    semap.save()
    return HttpResponse('Reset the queue')
