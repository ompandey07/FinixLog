# Authentication and model imports
from django.contrib.auth import authenticate, login , logout
from .models import Employee,Inquiry,Cheque,ActivityLog , BlogPost
from database.models import Crm_Contacts
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
import shutil
from django.utils import timezone
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .utils import create_log
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods






#! ----------------------------------------------------------------------- Views Start Here -----------------------------------------------------------------------



CustomUser = get_user_model()

# Custom decorator to prevent admin access to certain views
def prevent_admin_access(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            # Option 1: Redirect to another page
            return redirect('admin_dashboard')  # Replace with the desired route

            # Option 2: Return a forbidden response
            # return HttpResponseForbidden("You are not allowed to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# Function to create default admin user with predefined credentials
def create_default_user():
    """Creates a default user with specific credentials if not exists."""
    username = "admin@admin.com"
    password = "admin@1200"
    
    # Check if the user already exists
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=username, password=password)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for handling user login
def login_page(request):
    # Ensure the default user exists before processing login
    create_default_user()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                create_log('logged in', request.user)
                return redirect('admin_dashboard')

            elif hasattr(user, 'employee'):
                create_log('logged in', request.user)
                return redirect('users_dashboard')
            else:
                return redirect('default_dashboard')
        else:
            return render(request, "index.html", {'error': 'Username or Password did not match'})
    return render(request, "index.html")



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for handling user logout
def logout_view(request):
    logout(request)
    return redirect('login_page')



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# Utility function to check if user is superuser
def is_superuser(user):
    return user.is_superuser



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for admin dashboard, accessible only to superusers
@login_required
@user_passes_test(is_superuser)
def admin_dashboard(request):
    inquiries_count = Inquiry.objects.count()
    pending_cheques_count = Cheque.objects.filter(pending_status=True, diposited=False).count()
    employees_count = Employee.objects.count()
    contacts_count = Crm_Contacts.objects.count()
    
    context = {
        'inquiries_count': inquiries_count,
        'pending_cheques_count': pending_cheques_count,
        'employees_count': employees_count,
        'contacts_count': contacts_count,
    }
        
    return render(request, 'Admin/admin_dashboard.html',context)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for user dashboard, restricted from admin access
@login_required
@prevent_admin_access
def users_dashboard(request):
    user = request.user
    employee = Employee.objects.filter(user=user).first() 
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

    context = {
        'inquiries_count': inquiries_count,
        'pending_cheques_count': pending_cheques_count,
        'employees_count': employees_count,
        'employee': employee,
        'contacts_count': contacts_count,
    }    
    return render(request, "Users/users_dashboard.html", context)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for adding new employees, accessible only to superusers
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

        if password != confirm_password:
            return render(request, 'Admin/add_employee.html', {'error': 'Passwords do not match'})

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.is_employee = True
        user.save()

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
        create_log(f"Created new employee {first_name} {last_name}", request.user)
        return redirect('admin_dashboard')
    return render(request, 'Admin/add_employee.html')



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for adding new cheques
@login_required
def add_cheque(request):
    all_employees = Employee.objects.all()
    if request.method == 'POST':
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
        
        cheque.save()
        create_log(f"Added Cheque of '{company_name}' with cheque no: '{cheque_number}' ", request.user)
        return redirect('due_cheque_reports')

    context = {}
    if request.user.is_superuser:
        context['all_employees'] = all_employees
    else:
        employee = Employee.objects.filter(user=request.user).first()
        context['all_employees'] = [employee] if employee else []

    return render(request, 'cheque/add_cheque.html',context)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for adding new inquiries
@login_required
def add_inquiry(request):
    all_employees = Employee.objects.all()

    if request.method == 'POST':
        date = request.POST.get('date')
        miti = request.POST.get('miti')
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        called_received_by = request.POST.get('called_received_by')
        remarks = request.POST.get('remarks')

        if not customer_name or not contact_number:
            return render(request, 'add_inquiry.html', {'error': 'Please fill in all required fields'})

        if len(all_employees) == 1 and not called_received_by:
            called_received_by = f"{all_employees.first().first_name} {all_employees.first().last_name}"

        employee = Employee.objects.filter(user=request.user).first()

        if not called_received_by:
            if employee:
                called_received_by = f"{employee.first_name} {employee.last_name}"
            elif len(all_employees) == 1:
                called_received_by = f"{all_employees.first().first_name} {all_employees.first().last_name}"

        inquiry = Inquiry(
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
        create_log(f"Added Inquiry from  '{customer_name}'", request.user)

        return redirect('inquiry_status')

    try:
        next_form_no = Inquiry.objects.latest('id').id + 1
    except Inquiry.DoesNotExist:
        next_form_no = 1

    context = {
        'next_form_no': next_form_no,
    }

    if request.user.is_superuser:
        context['all_employees'] = all_employees
    else:
        employee = Employee.objects.filter(user=request.user).first()
        context['all_employees'] = [employee] if employee else []

    return render(request, 'inquiry/add_inquiry.html', context)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for updating existing inquiries
@login_required
def update_inquiry(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    all_employees = Employee.objects.all()

    if request.method == 'POST':
        inquiry.form_no = inquiry_id
        inquiry.date = request.POST.get('date')
        inquiry.customer_name = request.POST.get('customer_name')
        inquiry.company_name = request.POST.get('company_name')
        inquiry.contact_number = request.POST.get('contact_number')
        inquiry.address = request.POST.get('address')
        inquiry.called_received_by = request.POST.get("called_received_by", inquiry.called_received_by)
        inquiry.remarks = request.POST.get('remarks')
        
        inquiry.save()
        create_log(f"Updated Inquiry of customer '{inquiry.customer_name}' from company '{inquiry.company_name}' ", request.user)

        return redirect('inquiry_status')
    context = {
        'inquiry': inquiry,
        'all_employees': all_employees,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'inquiry/update_inquiry.html',context)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for displaying inquiry status
@login_required
def inquiry_status(req):
    all_employees = Employee.objects.all()

    if req.user.is_superuser:
        all_inquiry = Inquiry.objects.all()
        context = {
            'all_inquiry': all_inquiry,
            'is_superuser': True,
            'all_employees': all_employees,
        }
    else:
        employee = Employee.objects.filter(user=req.user).first()
        context = {
            'is_superuser': False,
            'all_employees': [employee] if employee else [],
        }

        if employee:
            employee_full_name = f"{employee.first_name} {employee.last_name}"
            all_inquiry = Inquiry.objects.filter(called_received_by__icontains=employee_full_name)
        else:
            all_inquiry = Inquiry.objects.none()

        context['all_inquiry'] = all_inquiry

    return render(req, "inquiry/inquiry_status.html", context)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for updating inquiry status
@login_required
def update_inquiry_status(req, inquiry_id):
    inquiry = Inquiry.objects.get(id=inquiry_id)
    
    if req.method == "POST":
        status = req.POST.get("status_of_inquiry")
        inquiry.status = status
        inquiry.save()
        create_log(f"Status of {inquiry.customer_name}'s inquiry changed to {status}", req.user)

        return redirect('inquiry_status')
    return redirect('inquiry_status')



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for deleting inquiries (admin only)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_inquiry(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    inquiry.delete()  
    create_log(f"deleted inquiry of customer '{inquiry.customer_name}' and company '{inquiry.company_name}'   ", request.user)
    return redirect('inquiry_status')



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for managing employees (admin only)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_employee(req):
    all_employees = Employee.objects.all()
    context = {
        'all_employees': all_employees
    }
    return render (req , "Admin/manage_employee.html",context)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for updating employee information (admin only)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    user = employee.user

    if request.method == 'POST':
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.email = request.POST.get('email')
        employee.address = request.POST.get('address')
        employee.contact = request.POST.get('contact')
        employee.age = request.POST.get('age')

        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password:
            if password != confirm_password:
                return render(request, 'Admin/update_employee.html', {
                    'employee': employee,
                    'error': 'Passwords do not match',
                    'username': user.username,
                })
            else:
                user.set_password(password)

        if 'profile_image' in request.FILES:
            employee.profile_image = request.FILES['profile_image']

        user.save()
        employee.save()
        create_log(f"employee of name '{employee.first_name}{employee.last_name}' is updated", request.user)

        return redirect('manage_employee')

    context = {
        'employee': employee,
        'username': user.username,
        'password': user.password
    }

    return render(request, 'Admin/update_employee.html', context)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for deleting employees (admin only)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    user = employee.user
    user.delete()
    create_log(f"employee of name '{employee.first_name}{employee.last_name}' is deleted", request.user)
    return redirect('manage_employee')



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for displaying cheque reports
@login_required
def cheque_reports(request):
    all_employees = Employee.objects.all()
    
    if request.user.is_superuser:
        all_cheques = Cheque.objects.filter(diposited=False)
    else:
        employee = Employee.objects.filter(user=request.user).first()
        if employee:
            full_name = f"{employee.first_name} {employee.last_name}"
            all_cheques = Cheque.objects.filter(handled_by=full_name, diposited=False)
        else:
            all_cheques = []

    context = {
        'all_cheques': all_cheques,
        'is_superuser': request.user.is_superuser,
        'all_employees': all_employees if request.user.is_superuser else [employee] if employee else [],
    }
    
    return render(request, "cheque/cheque_reports.html", context)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for displaying pending cheque reports
@login_required
def pending_cheque_reports(request):
    all_employees = Employee.objects.all()

    if request.user.is_superuser:
        all_cheques = Cheque.objects.filter(diposited=True, pending_status=True)
    else:
        employee = Employee.objects.filter(user=request.user).first()
        if employee:
            full_name = f"{employee.first_name} {employee.last_name}"
            all_cheques = Cheque.objects.filter(
                handled_by=full_name, diposited=True, pending_status=True
            )
        else:
            all_cheques = []

    context = {
        'all_cheques': all_cheques,
        'is_superuser': request.user.is_superuser,
        'all_employees': all_employees if request.user.is_superuser else [employee] if employee else [],
    }

    return render(request, "cheque/pending_cheque_reports.html", context)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for displaying completed cheque reports
@login_required
def completed_cheque_reports(request):
    all_employees = Employee.objects.all()

    if request.user.is_superuser:
        all_cheques = Cheque.objects.filter(diposited=True, pending_status=False)
    else:
        employee = Employee.objects.filter(user=request.user).first()
        if employee:
            full_name = f"{employee.first_name} {employee.last_name}"
            all_cheques = Cheque.objects.filter(
                handled_by=full_name, diposited=True, pending_status=False
            )
        else:
            all_cheques = []

    context = {
        'all_cheques': all_cheques,
        'all_employees': all_employees if request.user.is_superuser else [employee] if employee else [],
    }

    return render(request, "cheque/completed_cheque_reports.html", context)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for depositing cheques
@login_required
def deposit_cheque(request, cheque_id):
    cheque = get_object_or_404(Cheque, id=cheque_id)
    cheque.diposited = True
    cheque.save()
    create_log(f"cheque of company '{cheque.company_name}' disposited ", request.user)

    return JsonResponse({'status': 'success'}) 



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for updating cheque status
@login_required
def cheque_update_status(request, cheque_id):
    cheque = get_object_or_404(Cheque, id=cheque_id)
    
    if request.method == "POST":
        cheque_pending_status = request.POST.get("cheque_pending_status")
        if cheque_pending_status == "completed":
            cheque.pending_status = False
            create_log(f"cheque of company {cheque.company_name}'s status changed to pending  ", request.user)
        else:
            cheque.pending_status = True
            create_log(f"cheque of company {cheque.company_name}'s status changed to completed  ", request.user)
        
        cheque.save()
        return redirect('pending_cheque_reports')  



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for user profile management
@login_required
@prevent_admin_access
def user_profile(request):
    employee = Employee.objects.filter(user=request.user).first()
    user = employee.user

    if request.method == 'POST':
        employee.email = request.POST.get('email')
        employee.address = request.POST.get('address')
        employee.contact = request.POST.get('contact')
        employee.age = request.POST.get('age')

        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password:
            if password != confirm_password:
                return render(request, "profile/user_profile.html", {
                    'employee': employee,
                    'error': 'Passwords do not match',
                    'username': user.username,
                })
            else:
                user.set_password(password)

        if 'profile_image' in request.FILES:
            employee.profile_image = request.FILES['profile_image']

        user.save()
        employee.save()
        create_log(f"employee profile updated of '{employee.first_name}{employee.last_name}'", request.user)

        return redirect('logout')

    context = {
        'employee': employee,
        'username': user.username,
        'password': user.password
    }

    return render(request, "profile/user_profile.html", context)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for database backup
def backup_database(request):
    if request.method == 'POST':
        database_path = settings.DATABASES['default']['NAME']
        backup_dir = os.path.join(settings.MEDIA_ROOT, 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        backup_filename = f"backup_{timestamp}.sqlite3"
        backup_path = os.path.join(backup_dir, backup_filename)

        shutil.copy2(database_path, backup_path)

        if os.path.exists(backup_path):
            create_log(f"backup created successfully  ", request.user)
            return JsonResponse({"message": "Database backup created successfully.", "backup_filename": backup_filename})
        else:
            create_log(f"Failed to create a backup  ", request.user)
            return JsonResponse({"message": "Failed to create a backup."}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=400)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for database restoration
def restore_database(request):
    if request.method == 'POST' and request.FILES.get('backup_file'):
        backup_file = request.FILES['backup_file']
        database_path = settings.DATABASES['default']['NAME']
        fs = FileSystemStorage()
        temp_backup_path = fs.save(backup_file.name, backup_file)
        temp_backup_full_path = fs.path(temp_backup_path)

        if os.path.exists(temp_backup_full_path):
            os.replace(temp_backup_full_path, database_path)
            create_log(f"Database restored successfully  ", request.user)
            return JsonResponse({"message": "Database restored successfully."})
        else:
            create_log(f"Backup file not found.  ", request.user)
            return JsonResponse({"message": "Backup file not found."}, status=404)

    return JsonResponse({"message": "No file uploaded or invalid request."}, status=400)



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for activity logs
def activity_log(request):
    if not ActivityLog.objects.exists():
        ActivityLog.objects.create(task="System Initialized", user=request.user, timestamp=timezone.now())

    logs = ActivityLog.objects.all().order_by('-timestamp')
    return render(request, 'Admin/activity_log.html', {'logs': logs})



#? -------------------------------------------------------------------------------------------------------------------------------------------------------




# View for access denied error
def error_acces_denied(request):
    return render(request, '404.html')



#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for post arena log
@login_required
def post_arena_log_view(request, post_id=None):
    if not request.user.is_superuser and request.user.username != "admin@admin.com":
        return redirect('error_acces_denied')

    post = None  # Initialize post as None in case it's not found

    if post_id:
        # Check if post_id is provided (for editing)
        post = get_object_or_404(BlogPost, id=post_id)

    if request.method == 'POST':
        try:
            # Extract form data
            title = request.POST.get('title')
            content = request.POST.get('description')
            category = request.POST.get('category')
            new_image = request.FILES.get('imageInput')

            # Validate required fields
            if not all([title, category]):
                messages.error(request, 'Title and category are required')
                return render(request, 'Admin/PublishBlog.html', {
                    'categories': BlogPost.CATEGORY_CHOICES,
                    'post': post  # Pass post to the template for editing
                })

            if post:
                # Update existing post
                post.title = title
                post.content = content
                post.category = category.upper()
                if new_image:
                    post.image = new_image
                post.save()
                return render(request, 'Admin/PublishBlog.html', {
                    'categories': BlogPost.CATEGORY_CHOICES,
                    'post': post,
                    'success_message': 'Blog post updated successfully!',
                    'is_published': False
                })
            else:
                # Create new post
                BlogPost.objects.create(
                    title=title,
                    content=content,
                    category=category.upper(),
                    image=new_image if new_image else None,
                    author=request.user
                )
                return render(request, 'Admin/PublishBlog.html', {
                    'categories': BlogPost.CATEGORY_CHOICES,
                    'success_message': 'Blog post published successfully!',
                    'is_published': True
                })

        except Exception as e:
            messages.error(request, f'Error with blog post: {str(e)}')

    return render(request, 'Admin/PublishBlog.html', {
        'categories': BlogPost.CATEGORY_CHOICES,
        'post': post  # Pass post to the template for editing if it's provided
    })




#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for manage blog posts
@login_required
def manage_blog_view(request):
    if not request.user.is_superuser and request.user.username != "admin@admin.com":
        return redirect('error_acces_denied')

    posts = BlogPost.objects.select_related('author').all()
    categories = dict(BlogPost.CATEGORY_CHOICES)
    return render(request, 'Admin/ManageBlogs.html', {'posts': posts, 'categories': categories})




#? -------------------------------------------------------------------------------------------------------------------------------------------------------

# View for delete blog posts
@require_http_methods(["GET", "POST"]) # type: ignore
def delete_post(request, post_id):
    try:
        post = get_object_or_404(BlogPost, id=post_id)
        post.delete()
        # Redirect to the blog management page after deletion
        return redirect('manage_blog_view')
    except Exception as e:
        # Handle errors gracefully
        return redirect('manage_blog_view', error="Failed to delete post.")
