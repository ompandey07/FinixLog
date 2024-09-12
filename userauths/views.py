from django.contrib.auth import authenticate, login , logout
from .models import Employee,Inquiry,Cheque
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

    




@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_cheque(request):
    all_employees = Employee.objects.all()

    if request.method == 'POST':
        # Get data from the form submission
        handled_by = request.user
        company_name = request.POST.get('companyName')
        bank_name = request.POST.get('bankName')
        cheque_number = request.POST.get('chequeNumber')
        cheque_amount = request.POST.get('chequeAmount')
        remarks = request.POST.get('remarks')
        cheque_date = request.POST.get('chequeDate')
        mit = request.POST.get('mit')
        reminder_email = request.POST.get('reminderEmail')
        extra_reminder_email = request.POST.get('extraReminderEmail')

        # Create a new Cheque instance
        cheque = Cheque(
            handled_by=handled_by,
            company_name=company_name,
            bank_name=bank_name,
            cheque_number=cheque_number,
            cheque_amount=cheque_amount,
            remarks=remarks,
            cheque_date=cheque_date,
            mit=mit,
            reminder_email=reminder_email,
            extra_reminder_email=extra_reminder_email
        )
        
        # Save the cheque instance to the database
        cheque.save()

        # Redirect to a success page or return to form with a success message
        return redirect('add_cheque')  # Replace with your actual success URL
    context = {
        
    }
     # Check if the user is a superuser or an employee
    if request.user.is_superuser:
        context['all_employees'] = all_employees
    else:
        # If the user is not an admin, filter to only their employee
        employee = Employee.objects.filter(user=request.user).first()
        context['all_employees'] = [employee] if employee else []  # Ensure there's a list


    # Render the form in GET request
    return render(request, 'cheque/add_cheque.html',context)

    
    
    
    
@login_required
def add_inquiry(request):
    all_employees = Employee.objects.all()

    if request.method == 'POST':
        # Get data from the form submission
        date = request.POST.get('date')
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        called_received_by = request.POST.get('called_received_by')
        remarks = request.POST.get('remarks')

        # Validate data (add your validation logic here as needed)
        if not customer_name or not contact_number:
            return render(request, 'add_inquiry.html', {'error': 'Please fill in all required fields'})

        # If the select is disabled (only one employee), set called_received_by to that employee's name
        if len(all_employees) == 1 and not called_received_by:
            called_received_by = f"{all_employees.first().first_name} {all_employees.first().last_name}"


        # Get the employee associated with the logged-in user
        employee = Employee.objects.filter(user=request.user).first()

        # If no called_received_by is provided, set it to the employee's first name
        if not called_received_by:
            if employee:
                called_received_by = f"{employee.first_name} {employee.last_name}"  # Concatenate first and last name
            elif len(all_employees) == 1:
                called_received_by = f"{all_employees.first().first_name} {all_employees.first().last_name}"

        # Save the inquiry to the database
        inquiry = Inquiry(
            # form_no=form_no,
            date=date,
            customer_name=customer_name,
            company_name=company_name,
            contact_number=contact_number,
            address=address,
            called_received_by=called_received_by,
            remarks=remarks
        )
        inquiry.save()

        # Redirect to a success page or return to form with success message
        return redirect('inquiry_status')  # Make sure to replace 'success_page' with your actual redirect URL

    # Calculate the next available form number (inquiry id)
    try:
        next_form_no = Inquiry.objects.latest('id').id + 1
    except Inquiry.DoesNotExist:
        next_form_no = 1  # If no inquiries exist, the form_no starts from 1

    context = {
        'next_form_no': next_form_no,
    }

    # Check if the user is a superuser or an employee
    if request.user.is_superuser:
        context['all_employees'] = all_employees
    else:
        # If the user is not an admin, filter to only their employee
        employee = Employee.objects.filter(user=request.user).first()
        context['all_employees'] = [employee] if employee else []  # Ensure there's a list

    # Render the form in GET request
    return render(request, 'inquiry/add_inquiry.html', context)


@login_required
# @user_passes_test(lambda u: u.is_superuser)
def update_inquiry(request,inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    all_employees = Employee.objects.all()
    

    if request.method == 'POST':
        # Get data from the form submission
        inquiry.form_no = inquiry_id
        inquiry.date = request.POST.get('date')
        inquiry.customer_name = request.POST.get('customer_name')
        inquiry.company_name = request.POST.get('company_name')
        inquiry.contact_number = request.POST.get('contact_number')
        inquiry.address = request.POST.get('address')
        inquiry.called_received_by = request.POST.get("called_received_by", inquiry.called_received_by)  # Keep existing value if not provided
        inquiry.remarks = request.POST.get('remarks')

        # Validate data (add your validation logic here as needed)
        
        inquiry.save()
        

        # Redirect to a success page or return to form with success message
        return redirect('inquiry_status')  # Make sure to replace 'success_page' with your actual redirect URL
    context = {
        'inquiry': inquiry,
        'all_employees': all_employees,
        'is_superuser': request.user.is_superuser,  # Add this line

    }
    # Render the form in GET request
    return render(request, 'inquiry/update_inquiry.html',context)



@login_required
# @user_passes_test(lambda u: u.is_superuser)
def inquiry_status(req):
    all_inquiry = Inquiry.objects.all()
    context = {
        'all_inquiry': all_inquiry,
        'is_superuser': req.user.is_superuser,  # Add this line

    }
    return render (req , "inquiry/inquiry_status.html",context)




@login_required
def update_inquiry_status(req, inquiry_id):
    inquiry = Inquiry.objects.get(id=inquiry_id)
    
    if req.method == "POST":
        status = req.POST.get("status_of_inquiry")
        inquiry.is_completed = (status == "completed")  # Set is_completed based on selected status
        inquiry.save()
        return redirect('inquiry_status')  # Redirect back to the inquiry status page

    return redirect('inquiry_status')  # Handle GET requests



@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_inquiry(request, inquiry_id):
    # Get the employee object based on the ID
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)

    inquiry.delete()  

    # Redirect back to the manage employee page or any other page
    return redirect('inquiry_status')





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




