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


]