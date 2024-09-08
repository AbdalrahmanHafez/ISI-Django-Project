from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import OfficerForm
from django.http import JsonResponse, HttpResponse
from django.views import generic
from django.urls import reverse_lazy, reverse
import json
from . import filters


def officers_home_view(request):

    context= {
        'ranks':Rank.objects.all(),
        'form': OfficerForm(),
        'officers_filter': filters.OfficerFilter(request.GET)
    }

    return render(request, 'officers_affairs/home.html', context)


def officers_add(request, pk= None): # creates or Updates an officer
    if pk:
        officer = get_object_or_404(Officer, pk= pk)
        if request.method == "POST":
            form = OfficerForm(request.POST, request.FILES, instance= officer)
            if form.is_valid():
                form.instance.updated_by = request.user
                form.save()
                return HttpResponse(
                    status=204,
                    headers={
                        'HX-Trigger': json.dumps({
                            "showMessage": "تم تعديل ضابط",
                            "officer_list_changed": None
                        })
                    })
        else: # GET
            form = OfficerForm(instance= officer)
    
    # No PK, Create New
    elif request.method == "POST":
        form = OfficerForm(request.POST, request.FILES)
        if form.is_valid():
            if form.instance.pk == None: # if New 
                form.instance.created_by = request.user
            form.instance.updated_by = request.user
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "showMessage": "تم اضافة ضابط",
                        "officer_list_changed": None
                    })
                })

    else: # Empty Create
        form = OfficerForm()


    return render(request, "officers_affairs/officer_add.html", {'form': form})


def officers_view(request):
    context ={
        'ranks':Rank.objects.all(),
        'officers': Officer.objects.order_by('-rank'),
    }
    return render(request, 'officers_affairs/officers.html', context)


class officers_delete(generic.DeleteView):
    model = Officer

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse( status=204, headers={
                    'HX-Trigger': json.dumps({
                        "showMessage": "تم حذف ضابط",
                        "officer_list_changed": None
                    }) })

def officers_list(request):
    ctx={
        'officers_filter': filters.OfficerFilter(request.GET)
    }
    return render(request, 'officers_affairs/officer_list.html', ctx)
