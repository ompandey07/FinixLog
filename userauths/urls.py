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
    path('actyvity_log/', views.actyvity_log , name="actyvity_log"),
    path('manage_employee/', views.manage_employee , name="manage_employee"),
    path('update_employee/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),

    path('logout/', views.logout_view, name='logout'),



    # Users & Users Controls 
    path('users_dashboard/', views.users_dashboard , name="users_dashboard"),


    
]

# Serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


