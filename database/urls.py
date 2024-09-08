from django.contrib import admin
from django.urls import path
from database import views
urlpatterns = [

    # Lgins & Registations 
    path('login_page/', views.login_page , name="login_page"),


    # admin & admin controls 
    path('admin_dashboard/', views.admin_dashboard , name="admin_dashboard"),
    path('add_employe/', views.add_employe , name="add_employe"),
    path('actyvity_log/', views.actyvity_log , name="actyvity_log"),


    # Users & Users Controls 
    path('users_dashboard/', views.users_dashboard , name="users_dashboard"),

    

    # contacts and configs 
    path('create_contact/', views.create_contact, name='create_contact'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit/<int:contact_id>/', views.edit, name='edit'),


    # Notes & Configs 
    path('create_notes/', views.create_notes, name='create_notes'),
    path('delete_note/<int:id>', views.delete_note, name='delete_note'),


    # Calander & Configs 
    path('calendar/', views.calendar_setup, name='calendar'),
    path('add-event/', views.add_event, name='add_event'),
    path('update-event/<int:event_id>/', views.update_event, name='update_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
]