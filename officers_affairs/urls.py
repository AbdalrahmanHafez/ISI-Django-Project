from django.urls import path
from django.views import generic
from . import views
from . import models

urlpatterns = [
   
    path('officers_home/', views.officers_home_view, name='home'),
    path('listOfficers/', generic.ListView.as_view(model= models.Officer), name="listOfficers"),
    path('officers/', views.officers_view, name='officers'),
    # path('delete_officers/', views.officers_delete_view, name='delete'),
    # path('update_officers/', views.officers_update_view, name='update'),
    # Fragments
    path('addOfficer/', views.addOfficer, name="addOfficer" ),
]
