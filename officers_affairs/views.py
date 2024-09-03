from django.shortcuts import render
from .models import *
from .forms import OfficerForm
from django.http import JsonResponse, HttpResponse
import json



def officers_home_view(request):
    context ={
        'ranks':Rank.objects.all(),
        'officer_list':Officer.objects.all(),
        'form': OfficerForm()
    }
    return render(request, 'officers_affairs/home.html', context)





def addOfficer(request):
    if request.method == "POST":
        form = OfficerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "showMessage": f"Officer added",
                        "officer_list_changed": None
                    })
                })

    else:
        form = OfficerForm()

    return render(request, "officers_affairs/addOfficer.html", {'form': form})


def officers_view(request):
    context ={
        'ranks':Rank.objects.all(),
        'officers': Officer.objects.order_by('-rank'),
    }
    return render(request, 'officers_affairs/officers.html', context)


# def officers_delete_view(request):
#     return render(request, 'officers_affairs/delete.html')


# def officers_update_view(request):
#     return render(request, 'officers_affairs/update.html')