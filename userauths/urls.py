from django.contrib import admin
from django.urls import path , include
from userauths import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


urlpatterns = [
    path('', views.login_page , name="login_page"),


    # admin & admin controls 
    path('admin_dashboard/', views.admin_dashboard , name="admin_dashboard"),
    path('add_employee/', views.add_employee , name="add_employee"),
    path('add_inquiry/', views.add_inquiry , name="add_inquiry"),
    path('actyvity_log/', views.actyvity_log , name="actyvity_log"),
    path('manage_employee/', views.manage_employee , name="manage_employee"),
    path('inquiry_status/', views.inquiry_status , name="inquiry_status"),
    path('update_inquiry/<int:inquiry_id>/', views.update_inquiry, name='update_inquiry'),
    path('update_inquiry_status/<int:inquiry_id>/', views.update_inquiry_status, name='update_inquiry_status'),

    path('add_cheque/', views.add_cheque , name="add_cheque"),
    path('due_cheque_reports/', views.cheque_reports , name="due_cheque_reports"),
    path('pending_cheque_reports/', views.pending_cheque_reports , name="pending_cheque_reports"),
    path('completed_cheque_reports/', views.completed_cheque_reports , name="completed_cheque_reports"),
    path('cheque/deposit/<int:cheque_id>/', views.deposit_cheque, name='deposit_cheque'),
    path('cheque/update-status/<int:cheque_id>/', views.cheque_update_status, name='cheque_update_status'),


    
    path('delete_inquiry/<int:inquiry_id>/', views.delete_inquiry, name='delete_inquiry'),
    path('update_employee/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),

    path('logout/', views.logout_view, name='logout'),



    # Users & Users Controls 
    path('users_dashboard/', views.users_dashboard , name="users_dashboard"),


    
]

# Serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


