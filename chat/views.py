from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def control(request, room_name):
    return render(request, 'control.html', {})
