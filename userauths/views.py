from django.contrib.auth import authenticate, login , logout
from .models import Employee,Inquiry,Cheque
from database.models import Crm_Contacts
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.http import HttpResponseRedirect
import shutil
from django.utils import timezone
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage







CustomUser = get_user_model()

def prevent_admin_access(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            # Option 1: Redirect to another page
            return redirect('admin_dashboard')  # Replace with the desired route

            # Option 2: Return a forbidden response
            # return HttpResponseForbidden("You are not allowed to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view



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
    inquiries_count = Inquiry.objects.count()
    pending_cheques_count = Cheque.objects.filter(pending_status=True, diposited=False).count()  # Adjust the filter as necessary
    employees_count = Employee.objects.count()
    contacts_count = Crm_Contacts.objects.count()
    

    # Prepare the context
    context = {
        'inquiries_count': inquiries_count,
        'pending_cheques_count': pending_cheques_count,
        'employees_count': employees_count,
        'contacts_count': contacts_count,
    }
    
    
    return render(request, 'Admin/admin_dashboard.html',context)





@login_required
@prevent_admin_access
def users_dashboard(request):
    user = request.user
    employee = Employee.objects.filter(user=user).first() 
  
    # inquiries_count = Inquiry.objects.filter(called_received_by=request.user).count
    # pending_cheques_count = Cheque.objects.filter(pending_status=True).count()  # Adjust the filter as necessary
    employees_count = Employee.objects.count()
    contacts_count = Crm_Contacts.objects.count()

    employee = Employee.objects.filter(user=request.user).first()
    if employee:
            full_name = f"{employee.first_name} {employee.last_name}"
            pending_cheques_count = Cheque.objects.filter(
                handled_by=full_name, diposited=False
            ).count()
            inquiries_count = Inquiry.objects.filter(
                called_received_by=full_name
            ).count()

    

    # Prepare the context
    context = {
        'inquiries_count': inquiries_count,
        'pending_cheques_count': pending_cheques_count,
        'employees_count': employees_count,
        'employee': employee,
        'contacts_count': contacts_count,


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
# @user_passes_test(lambda u: u.is_superuser)
def add_cheque(request):
    all_employees = Employee.objects.all()

    if request.method == 'POST':
        # Get data from the form submission
        handled_by = request.POST.get('handled_by')


        company_name = request.POST.get('companyName')
        bank_name = request.POST.get('bankName')
        cheque_number = request.POST.get('chequeNumber')
        cheque_amount = request.POST.get('chequeAmount')
        remarks = request.POST.get('remarks')
        cheque_date = request.POST.get('cheque_date')
        cheque_miti = request.POST.get('cheque_miti')
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
            cheque_miti=cheque_miti,
            reminder_email=reminder_email,
            extra_reminder_email=extra_reminder_email
        )
        
        # Save the cheque instance to the database
        cheque.save()

        # Redirect to a success page or return to form with a success message
        return redirect('due_cheque_reports')  # Replace with your actual success URL
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
        miti = request.POST.get('miti')
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
            miti=miti,
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



# @login_required
# # @user_passes_test(lambda u: u.is_superuser)
# def inquiry_status(req):
#     all_inquiry = Inquiry.objects.all()
#     all_employees = Employee.objects.all()

#     context = {
#         'all_inquiry': all_inquiry,
#         'is_superuser': req.user.is_superuser,  # Add this line

#     }

    

#     # Check if the user is a superuser or an employee
#     if req.user.is_superuser:
#         context['all_employees'] = all_employees
#     else:
#         # If the user is not an admin, filter to only their employee
#         employee = Employee.objects.filter(user=req.user).first()
#         context['all_employees'] = [employee] if employee else []  # Ensure there's a list
#     return render (req , "inquiry/inquiry_status.html",context)


@login_required
def inquiry_status(req):
    # Get all employees
    all_employees = Employee.objects.all()

    # Check if the user is a superuser
    if req.user.is_superuser:
        all_inquiry = Inquiry.objects.all()  # All inquiries for superusers
        context = {
            'all_inquiry': all_inquiry,
            'is_superuser': True,
            'all_employees': all_employees,
        }
    else:
        # If the user is not a superuser, filter inquiries by the employee they are associated with
        employee = Employee.objects.filter(user=req.user).first()
        context = {
            'is_superuser': False,
            'all_employees': [employee] if employee else [],
        }

        # Filter inquiries based on called_received_by matching the employee's first and last name
        if employee:
            # Split the employee's full name into first and last name
            employee_full_name = f"{employee.first_name} {employee.last_name}"
            
            # Filter inquiries where called_received_by matches the employee's full name
            all_inquiry = Inquiry.objects.filter(called_received_by__icontains=employee_full_name)
        else:
            all_inquiry = Inquiry.objects.none()  # No inquiries if there's no associated employee

        context['all_inquiry'] = all_inquiry

    return render(req, "inquiry/inquiry_status.html", context)





# @login_required
# def update_inquiry_status(req, inquiry_id):
#     inquiry = Inquiry.objects.get(id=inquiry_id)
    
#     if req.method == "POST":
#         status = req.POST.get("status_of_inquiry")
#         inquiry.is_completed = (status == "completed")  # Set is_completed based on selected status
#         inquiry.save()
#         return redirect('inquiry_status')  # Redirect back to the inquiry status page

#     return redirect('inquiry_status')  # Handle GET requests

@login_required
def update_inquiry_status(req, inquiry_id):
    inquiry = Inquiry.objects.get(id=inquiry_id)
    
    if req.method == "POST":
        status = req.POST.get("status_of_inquiry")
        inquiry.status = status  # Set status based on selected value
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




@login_required
# @user_passes_test(lambda u: u.is_superuser)
# def cheque_reports(request):
#     all_cheques = Cheque.objects.filter(diposited=False)
#     all_employees = Employee.objects.all()
#     context = {
#         'all_cheques': all_cheques,
#         'is_superuser': request.user.is_superuser,  


#     }

#     # Check if the user is a superuser or an employee
#     if request.user.is_superuser:
#         context['all_employees'] = all_employees
#     else:
#         # If the user is not an admin, filter to only their employee
#         employee = Employee.objects.filter(user=request.user).first()
#         context['all_employees'] = [employee] if employee else []  # Ensure there's a list


    
#     return render (request , "cheque/cheque_reports.html",context)

def cheque_reports(request):
    all_employees = Employee.objects.all()
    
    # Check if the user is a superuser or an employee
    if request.user.is_superuser:
        # Superuser sees all cheques
        all_cheques = Cheque.objects.filter(diposited=False)
    else:
        # Non-superusers (employees) only see cheques handled by them
        employee = Employee.objects.filter(user=request.user).first()
        if employee:
            full_name = f"{employee.first_name} {employee.last_name}"
            all_cheques = Cheque.objects.filter(handled_by=full_name, diposited=False)
        else:
            all_cheques = []  # No employee record, no cheques to show

    context = {
        'all_cheques': all_cheques,
        'is_superuser': request.user.is_superuser,
        'all_employees': all_employees if request.user.is_superuser else [employee] if employee else [],
    }
    
    return render(request, "cheque/cheque_reports.html", context)

@login_required
# @user_passes_test(lambda u: u.is_superuser)
# def pending_cheque_reports(request):
#     all_cheques = Cheque.objects.filter(diposited=True,pending_status=True)
#     all_employees = Employee.objects.all()

#     context = {
#         'all_cheques': all_cheques,
#         'is_superuser': request.user.is_superuser,  


#     }

#     # Check if the user is a superuser or an employee
#     if request.user.is_superuser:
#         context['all_employees'] = all_employees
#     else:
#         # If the user is not an admin, filter to only their employee
#         employee = Employee.objects.filter(user=request.user).first()
#         context['all_employees'] = [employee] if employee else []  # Ensure there's a list
#     return render (request , "cheque/pending_cheque_reports.html",context)



@login_required
def pending_cheque_reports(request):
    all_employees = Employee.objects.all()

    # Check if the user is a superuser or an employee
    if request.user.is_superuser:
        # Superuser sees all pending cheques
        all_cheques = Cheque.objects.filter(diposited=True, pending_status=True)
    else:
        # Non-superusers (employees) only see pending cheques handled by them
        employee = Employee.objects.filter(user=request.user).first()
        if employee:
            full_name = f"{employee.first_name} {employee.last_name}"
            all_cheques = Cheque.objects.filter(
                handled_by=full_name, diposited=True, pending_status=True
            )
        else:
            all_cheques = []  # No employee record, no cheques to show

    context = {
        'all_cheques': all_cheques,
        'is_superuser': request.user.is_superuser,
        'all_employees': all_employees if request.user.is_superuser else [employee] if employee else [],
    }

    return render(request, "cheque/pending_cheque_reports.html", context)



@login_required
# @user_passes_test(lambda u: u.is_superuser)
# def completed_cheque_reports(request):
#     all_cheques = Cheque.objects.filter(diposited=True,pending_status=False)
#     all_employees = Employee.objects.all()

#     context = {
#         'all_cheques': all_cheques,

#     }

#     # Check if the user is a superuser or an employee
#     if request.user.is_superuser:
#         context['all_employees'] = all_employees
#     else:
#         # If the user is not an admin, filter to only their employee
#         employee = Employee.objects.filter(user=request.user).first()
#         context['all_employees'] = [employee] if employee else []  # Ensure there's a list
#     return render (request , "cheque/completed_cheque_reports.html",context)

def completed_cheque_reports(request):
    all_employees = Employee.objects.all()

    # Check if the user is a superuser or an employee
    if request.user.is_superuser:
        # Superuser sees all completed cheques
        all_cheques = Cheque.objects.filter(diposited=True, pending_status=False)
    else:
        # Non-superusers (employees) only see completed cheques handled by them
        employee = Employee.objects.filter(user=request.user).first()
        if employee:
            full_name = f"{employee.first_name} {employee.last_name}"
            all_cheques = Cheque.objects.filter(
                handled_by=full_name, diposited=True, pending_status=False
            )
        else:
            all_cheques = []  # No employee record, no cheques to show

    context = {
        'all_cheques': all_cheques,
        'all_employees': all_employees if request.user.is_superuser else [employee] if employee else [],
    }

    return render(request, "cheque/completed_cheque_reports.html", context)



@login_required
# @user_passes_test(lambda u: u.is_superuser)
def deposit_cheque(request, cheque_id):
    cheque = get_object_or_404(Cheque, id=cheque_id)
    cheque.diposited = True
    cheque.save()
    return JsonResponse({'status': 'success'}) 



@login_required
# @user_passes_test(lambda u: u.is_superuser)
def cheque_update_status(request, cheque_id):
    cheque = get_object_or_404(Cheque, id=cheque_id)
    
    if request.method == "POST":
        cheque_pending_status = request.POST.get("cheque_pending_status")
        if cheque_pending_status == "completed":
            cheque.pending_status = False
        else:
            cheque.pending_status = True
        
        cheque.save()
        return redirect('pending_cheque_reports')  



    
# @login_required
# @user_passes_test(lambda u: u.is_superuser)
def user_profile(request):
    
    return render (request , "profile/user_profile.html")



@login_required
@prevent_admin_access
def user_profile(request):
    # Get the employee object based on the ID
    employee = Employee.objects.filter(user=request.user).first()
    user = employee.user  # Get the related user

    if request.method == 'POST':
        # Get form data
        # employee.first_name = request.POST.get('first_name')
        # employee.last_name = request.POST.get('last_name')
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
                return render(request, "profile/user_profile.html", {
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
        return redirect('logout')

    # Pass the employee object to the template for displaying current data
    context = {
        'employee': employee,
        'username': user.username,  # Pass the username to the template
        'password': user.password


    }

    return render(request, "profile/user_profile.html", context)



def backup_database(request):
    if request.method == 'POST':
        # Define the path to your current SQLite database
        database_path = settings.DATABASES['default']['NAME']

        # Define the path for the backup file in the media folder
        backup_dir = os.path.join(settings.MEDIA_ROOT, 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Create a backup filename with a timestamp
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        backup_filename = f"backup_{timestamp}.sqlite3"
        backup_path = os.path.join(backup_dir, backup_filename)

        # Copy the database to the backup path
        shutil.copy2(database_path, backup_path)

        # Check if the backup file was created successfully
        if os.path.exists(backup_path):
            # Return the JSON response with a message and the filename
            return JsonResponse({"message": "Database backup created successfully.", "backup_filename": backup_filename})
        else:
            return JsonResponse({"message": "Failed to create a backup."}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=400)


def restore_database(request):
    if request.method == 'POST' and request.FILES.get('backup_file'):
        # Get the uploaded file
        backup_file = request.FILES['backup_file']

        # Define the path to the current SQLite database
        database_path = settings.DATABASES['default']['NAME']

        # Save the uploaded backup file temporarily
        fs = FileSystemStorage()
        temp_backup_path = fs.save(backup_file.name, backup_file)
        temp_backup_full_path = fs.path(temp_backup_path)  # Get the full path of the saved backup

        # Check if the uploaded backup file exists
        if os.path.exists(temp_backup_full_path):
            # Replace the current database with the uploaded backup
            os.replace(temp_backup_full_path, database_path)
            return JsonResponse({"message": "Database restored successfully."})
        else:
            return JsonResponse({"message": "Backup file not found."}, status=404)

    return JsonResponse({"message": "No file uploaded or invalid request."}, status=400)