from django.urls import path

from . import views

urlpatterns = [
   
    path('officers_home/', views.officers_home_view, name='home'),
    path('officers/', views.officers_view, name='officers'),
    # path('delete_officers/', views.officers_delete_view, name='delete'),
    # path('update_officers/', views.officers_update_view, name='update'),
]
