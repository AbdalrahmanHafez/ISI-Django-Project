from django.shortcuts import render

# Create your views here.



def officers_home_view(request):
    return render(request, 'officers_affairs/home.html')

def officers_view(request):
    return render(request, 'officers_affairs/officers.html')


# def officers_delete_view(request):
#     return render(request, 'officers_affairs/delete.html')


# def officers_update_view(request):
#     return render(request, 'officers_affairs/update.html')