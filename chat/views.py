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
            messages.info(request, "Nesprávne používateľské meno alebo heslo!")

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
            messages.success(request, user + ", Váš účet bol úspešne vytvorený!")
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
            task.lastQueueNum = 0
            task.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'addSemaphore.html', context)


def contact(request):
    return render(request, 'contact.html', {})


@login_required(login_url='mainpage')
def control(request, pk_test):
    semap = Semaphore.objects.get(controlUrl=pk_test)
    semapClients = QueueClient.objects.filter(semap=semap, queueNum__gt=semap.lastQueueNum)
    first = semapClients.first()

    return render(request, 'control.html', {'semap': semap, 'pk_test': pk_test, 'semapClients': semapClients, 'first': first})


def semaphore(request, pk_test):
    semap = Semaphore.objects.get(controlUrl=pk_test)
    semapClients = QueueClient.objects.filter(semap=semap, queueNum__gt=semap.lastQueueNum)
    numQueueClients = semapClients.count()
    # deviceCookie = request.COOKIES['device']

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
def joinQueueUrl(request, pk_test, client_name):
    semap = Semaphore.objects.get(controlUrl=pk_test)
    device = request.COOKIES['device']
    lastallqueue = QueueClient.objects.last()     # last client in whole DB

    # try get the last client in database
    if lastallqueue == None:
        firstclient, created = QueueClient.objects.get_or_create(device=device, semap=semap, queueNum=1, clientName=client_name, clientNumber=0)
        response = {
            'msg': "Change number of queue first time"
        }

        return JsonResponse(response)

    else:
        lastClientNumber = lastallqueue.queueNum  # last magic number in whole DB
        newLastClientNumber = lastClientNumber + 1

    semapClients = QueueClient.objects.filter(semap=semap, queueNum__gt=semap.lastQueueNum) # waiting clients
    numQueueClients = semapClients.count() # number of waiting clients in queue


    # check if the client is in DB
    try:
        client = QueueClient.objects.get(device=device, semap=semap, queueNum__gte=semap.lastQueueNum)
        response = {
            'msg': "You are already in the queue"
        }
    except:
        client, created = QueueClient.objects.get_or_create(device=device, semap=semap, queueNum=newLastClientNumber, clientName=client_name, clientNumber=numQueueClients)
        time = client.clientNumber * semap.time;
        response = {
            'msg': "Change number of queue",
            'num': str(numQueueClients),
            'clienttime': str(time),
        }

    return JsonResponse(response)


@csrf_exempt
def checkQueueUrl(request, pk_test):
    semap = Semaphore.objects.get(controlUrl=pk_test)
    semapClients = QueueClient.objects.filter(semap=semap, queueNum__gte=semap.lastQueueNum)
    device = request.COOKIES['device']

    try:
        client = semapClients.get(device=device)
        if client.queueNum == semap.lastQueueNum:
            response = {
                'msg': "SAME",
                'msgName': str(client.clientName),
                'msgNum': str(client.clientNumber),

            }
        else:
            time = client.Number * semap.time
            response = {
                'msg': "DIFFERENT",
                'msgName': str(client.clientName),
                'msgNum': str(client.clientNumber),
                'msgTime': str(time),
            }

    except:
        response = {
            'msg': "not in queue",
        }

    return JsonResponse(response)


@csrf_exempt
def helloQueueUrl(request, pk_test):
    device = request.COOKIES['device']
    semap = Semaphore.objects.get(controlUrl=pk_test)

    if semap.semOpen == False:
        response = {
            'msg': "Close now"
        }
        return JsonResponse(response)

    # check if the client is in DB
    try:
        client = QueueClient.objects.get(device=device, semap=semap, queueNum__gte=semap.lastQueueNum)
        response = {
            'msg': "You are already in the queue",
        }
    except:
        response = {
            'msg': "Not in queue"
        }

    return JsonResponse(response)


@csrf_exempt
def manageSemUrl(request, pk_test):
    semap = Semaphore.objects.get(controlUrl=pk_test)
    status = semap.semOpen

    if (status == False):
        semap.semOpen = True
        semap.save()
        response = {
            'msg': "Open semaphore"
        }
    elif (status == True):
        semap.semOpen = False
        semap.save()
        response = {
            'msg': "Close semaphore"
        }

    return JsonResponse(response)


@csrf_exempt
def editLastClient(request, pk_test):
    semap = Semaphore.objects.get(controlUrl=pk_test)
    semapClients = QueueClient.objects.filter(semap=semap, queueNum__gt=semap.lastQueueNum) # all clients in queue
    first = semapClients.first()    # first client in queue
    semap.lastQueueNum = first.queueNum     # magic number of first client save as number of last client in queue
    semap.save()
    response = {
        'msg': 'lastClient changed',
        'num': str(semap.lastQueueNum)
    }

    return JsonResponse(response)


@csrf_exempt
def editClientInfo(request, pk_test):
    device = request.COOKIES['device']
    semap = Semaphore.objects.get(controlUrl=pk_test)
    allclients = QueueClient.objects.filter(semap=semap, queueNum__gte=semap.lastQueueNum)
    client = allclients.get(device=device)

    newClientNumber = client.clientNumber - 1
    client.clientNumber = newClientNumber
    client.save()

    response = {
        'msgNum': str(newClientNumber)
    }
    return JsonResponse(response)


@csrf_exempt
def checkEmptyQueue(request, pk_test):
    semap = Semaphore.objects.get(controlUrl=pk_test)
    allclients = QueueClient.objects.filter(semap=semap, queueNum__gt=semap.lastQueueNum)
    count = allclients.count()

    if count == 0:
        response = {
            'msg': "Nobody in queue"
        }
    else:
        response = {
            'msg': "Someone in queue"
        }

    return JsonResponse(response)
