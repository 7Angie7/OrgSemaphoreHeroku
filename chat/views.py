from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def admin_page(request, room_name):
    return render(request, 'admin_page.html', {})
