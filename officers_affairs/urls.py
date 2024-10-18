from django.urls import path
from django.views import generic
from . import views
from . import models
from django.conf.urls.static import static
from myproject import settings

urlpatterns = [
    path('officers_home/', views.officers_home_view, name='home'),
    path('officers/', views.officers_view, name='officers'),
    # path('delete_officers/', views.officers_delete_view, name='delete'),
    # path('update_officers/', views.officers_update_view, name='update'),
    # Fragments
    path('officers_list/', views.officers_list, name="officers_list"),
    path('partial_officers/', views.partial_officers, name="partial_officers"),
    path('officers_add/', views.officers_add, name="officers_add" ),
    path('officers_add/<int:pk>', views.officers_add, name="officers_add" ),
    path('officers_delete/<int:pk>', views.officers_delete.as_view(), name="officers_delete" ),
    path('officer/<int:pk>/', views.officer_detail, name='officer_detail'),
    
    path('leave/create/', views.create_update_leave_request, name='create_leave_request'),
    path('leave/update/<int:pk>', views.create_update_leave_request, name='update_leave_request'),
    path('leave/requests/', views.leave_requests_list, name='leave_requests_list'),  # For leaders to see all requests
    path('leave/my-requests/', views.leave_requests, name='leave_requests'),  # For users to see only their requests
    path('leave/approve/<int:pk>/', views.approve_leave_request, name='approve_leave_request'),
    # path('calculate-leave-remaining/', views.calculate_leave_remaining, name='calculate_leave_remaining'),
    
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/mark_read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/check-new/', views.check_new_notifications, name='check_new_notifications'),
    
    path('notification_list/', views.notification_list, name='notification_list'),
    
    path('record_attendance/', views.record_attendance, name='record_attendance'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
    
    path('record_parade_attendance/', views.record_parade_attendance, name='record_parade_attendance'),
    path('parade_attendance_list/', views.parade_attendance_list, name='parade_attendance_list'),

    
    path('shifts/assign/', views.assign_shifts, name='assign_shifts'),
]
