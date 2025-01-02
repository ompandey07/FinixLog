from django.contrib import admin
from django.urls import path

from database import views
urlpatterns = [

    # Lgins & Registations 
    

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


    # Blogs & Configs
    path('blog/', views.blog_view, name='blog_view'),
]

