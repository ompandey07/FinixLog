from django.contrib.auth import authenticate, login , logout
from .models import Employee
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect



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
            elif hasattr(user, 'employee'):  # Check if user is an employee
                return redirect('users_dashboard')
            else:
                return redirect('default_dashboard')  # Redirect to some default page if neither admin nor employee
        else:
            return render(request, "index.html", {'error': 'Invalid credentials'})
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



@login_required
def users_dashboard(request):
    user = request.user
    employee = Employee.objects.filter(user=user).first() 
    context = {
        'employee': employee,
    }
    return render(request, "Users/users_dashboard.html", context)


CustomUser = get_user_model()

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_employee(request):
    if request.method == 'POST':
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


@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_employee(req):
    all_employees = Employee.objects.all()
    context = {
        'all_employees': all_employees
    }
    return render (req , "Admin/manage_employee.html",context)



@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_employee(request, employee_id):
    # Get the employee object based on the ID
    employee = get_object_or_404(Employee, id=employee_id)
    user = employee.user  # Get the related user

    if request.method == 'POST':
        # Get form data
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.email = request.POST.get('email')
        employee.address = request.POST.get('address')
        employee.contact = request.POST.get('contact')
        employee.age = request.POST.get('age')

        user.username = request.POST.get('username')  # Update the associated user's username
        user.email = request.POST.get('email')  # Update the associated user's email

        # Get the passwords from the form
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate password fields
        if password:  # Check if password field is provided
            if password != confirm_password:
                return render(request, 'Admin/update_employee.html', {
                    'employee': employee,
                    'error': 'Passwords do not match',  # Pass error message
                    'username': user.username,
                })
            else:
                # Only update the password if it is provided and valid
                user.set_password(password)

        # Handle profile image update (optional)
        if 'profile_image' in request.FILES:
            employee.profile_image = request.FILES['profile_image']

        # Save the updated data
        user.save()
        employee.save()

        # Redirect back to manage employee page or any other page
        return redirect('manage_employee')

    # Pass the employee object to the template for displaying current data
    context = {
        'employee': employee,
        'username': user.username,  # Pass the username to the template
        'password': user.password


    }

    return render(request, 'Admin/update_employee.html', context)





@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_employee(request, employee_id):
    # Get the employee object based on the ID
    employee = get_object_or_404(Employee, id=employee_id)

    # Delete the associated user and the employee
    user = employee.user
    user.delete()  # This will also delete the employee due to the OneToOneField

    # Redirect back to the manage employee page or any other page
    return redirect('manage_employee')




