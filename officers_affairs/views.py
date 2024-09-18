from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import *
from .forms import OfficerForm,RankForm
from django.http import JsonResponse, HttpResponse
from django.views import generic
from django.urls import reverse_lazy, reverse
import json
from . import filters



@permission_required('officers_affairs.view_rank', raise_exception=True)
def officers_home_view(request):
    
    if request.method == 'POST':
        add_rank = RankForm(request.POST, request.FILES)
        if add_rank.is_valid():
            add_rank.save()
            

    context= {
        'ranks':Rank.objects.all(),
        'form': OfficerForm(),
        'officers_filter': filters.OfficerFilter(request.GET),
        'count_officers_total': Officer.objects.count(),
        'count_officers_availble': Officer.objects.filter(unit_status__name="موجود").count(),
        'formrank':RankForm(),
    }

    return render(request, 'officers_affairs/home.html', context)


@login_required
@permission_required('officers_affairs.add_officer', raise_exception=True)
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
    search=Officer.objects.order_by('rank')
    title = None
    if 'search_name' in request.GET:
        title = request.GET.get('search_name')
        if title:
            search = search.filter(full_name__icontains=title)
    
    
    context ={
        'ranks':Rank.objects.all(),
        'officers': search,
    }
    return render(request, 'officers_affairs/officers.html', context)


class officers_delete(PermissionRequiredMixin, generic.DeleteView):
    permission_required = ('officers_affairs.delete_officer', )

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
        'ranks':Rank.objects.all(),
        'officers_filter': filters.OfficerFilter(request.GET),
    }
    return render(request, 'officers_affairs/officer_list.html', ctx)


def about(request):
    return render(request, 'about.html')


@login_required
def officer_add_view(request):
    if request.method == 'POST':
        form = OfficerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('officer_list')  # Redirect to officer list or other appropriate page
    else:
        form = OfficerForm()

    return render(request, 'officers_affairs/officer_add.html', {'form': form})