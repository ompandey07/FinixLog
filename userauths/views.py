from django.contrib.auth import authenticate, login , logout
from django.shortcuts import render, redirect
from .models import Employee
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test


CustomUser = get_user_model()

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.is_employee:
                return redirect('users_dashboard')
    return render(request, "index.html")


def logout_view(request):
    logout(request)
    return redirect('login_page')


def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def admin_dashboard(request):
    return render(request, 'Admin/admin_dashboard.html')



def users_dashboard(req):
    return render (req , "Users/users_dashboard.html")


CustomUser = get_user_model()

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def add_employee(request):
    if request.method == 'POST':
        # Extract data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        age = request.POST.get('age')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_image = request.FILES.get('profile_image')

        # Validate data
        if password != confirm_password:
            return render(request, 'Admin/add_employee.html', {'error': 'Passwords do not match'})

        # Create User
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.is_employee = True
        user.save()

        # Create Employee
        employee = Employee.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            contact=contact,
            age=age,
            profile_image=profile_image
        )

        return redirect('admin_dashboard')

    return render(request, 'Admin/add_employee.html')


def actyvity_log(req):
    return render (req , "Admin/activity_log.html")
