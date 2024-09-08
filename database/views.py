from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.



def login_page (req):
    return render (req, "index.html")


def admin_dashboard(req):
    return render (req , "Admin/admin_dashboard.html")

def add_employe(req):
    return render (req , 'Admin/add_employe.html')

def actyvity_log(req):
    return render (req , "Admin/activity_log.html")


def users_dashboard(req):
    return render (req , "Users/users_dashboard.html")