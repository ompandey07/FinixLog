from django.contrib import admin
from django.urls import path
from database import views
urlpatterns = [
    path('home/', views.home),
]