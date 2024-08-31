from django.shortcuts import render
from .models import *
# Create your views here.



def officers_home_view(request):
    context ={
        'officers':Officer.objects.all(),
    }
    return render(request, 'officers_affairs/home.html', context)

def officers_view(request):
    return render(request, 'officers_affairs/officers.html')


# def officers_delete_view(request):
#     return render(request, 'officers_affairs/delete.html')


# def officers_update_view(request):
#     return render(request, 'officers_affairs/update.html')