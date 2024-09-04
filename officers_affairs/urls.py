from django.urls import path
from django.views import generic
from . import views
from . import models

urlpatterns = [
    path('officers_home/', views.officers_home_view, name='home'),
    path('officers/', views.officers_view, name='officers'),
    # path('delete_officers/', views.officers_delete_view, name='delete'),
    # path('update_officers/', views.officers_update_view, name='update'),
    # Fragments
    path('officers_list/', generic.ListView.as_view(model= models.Officer), name="officers_list"),
    path('officers_add/', views.officers_add, name="officers_add" ),
    path('officers_add/<int:pk>', views.officers_add, name="officers_add" ),
    path('officers_delete/<int:pk>', views.officers_delete.as_view(), name="officers_delete" ),
]
