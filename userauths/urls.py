from django.contrib import admin
from django.urls import path , include
from userauths import views
urlpatterns = [
    path('login_page/', views.login_page , name="login_page"),


    # admin & admin controls 
    path('admin_dashboard/', views.admin_dashboard , name="admin_dashboard"),
    path('add_employee/', views.add_employee , name="add_employee"),
    path('actyvity_log/', views.actyvity_log , name="actyvity_log"),
    path('logout/', views.logout_view, name='logout'),



    # Users & Users Controls 
    path('users_dashboard/', views.users_dashboard , name="users_dashboard"),
]
