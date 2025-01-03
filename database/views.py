from django.shortcuts import render , redirect , get_object_or_404
from .models import Crm_Contacts , Crm_Notes , Event
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from userauths.models import Employee , BlogPost
from userauths.utils import create_log
import shutil
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers.json import DjangoJSONEncoder




#! --------------------------------------------------------------------------------Views Start Here--------------------------------------------------------------------------------

# Create Contact
def create_contact(request):
    if request.method == "POST":
        # Get form data from POST request
        contact_name = request.POST.get('contact_name')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        website = request.POST.get('website')
        designaton = request.POST.get('designaton')

        # Save the data to the database
        Crm_Contacts.objects.create(
            contact_name=contact_name,
            contact_number=contact_number,
            email=email,
            address=address,
            website=website,
            designaton=designaton
        )
        create_log(f"Contact Has Been Created", request.user)                
        return redirect('create_contact')    
    # For GET request, render the form and table
    contacts = Crm_Contacts.objects.all()  # Fetch all contacts to display in the table
    return render(request, "crm/Contacts.html", {'contacts': contacts})



#? ----------------------------------------------------------------------------------------------------------------------------
# Delete Contact
def delete (request , id):
    db=request.session.get('database_path')
    contact = Crm_Contacts.objects.get(id=id)
    contact.delete()
    return redirect ('create_contact')



#? ----------------------------------------------------------------------------------------------------------------------------
# Edit Contact
def edit(request, contact_id):
    db=request.session.get('database_path')
    contact = get_object_or_404(Crm_Contacts, id=contact_id)

    if request.method == 'POST':
        contact.contact_name = request.POST.get('contact_name')
        contact.contact_number = request.POST.get('contact_number')
        contact.email = request.POST.get('email')
        contact.address = request.POST.get('address')
        contact.website = request.POST.get('website')
        contact.designaton = request.POST.get('designaton')
        create_log(f"Contact Has Been Updated", request.user)
        contact.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



#? ----------------------------------------------------------------------------------------------------------------------------
# Create Notes
@login_required
def create_notes(request):
    # Handle note creation
    if request.method == "POST":
        note_title = request.POST.get('note_title')
        note_content = request.POST.get('note_content')
        # Associate the note with the logged-in user's employee record
        employee = Employee.objects.filter(user=request.user).first()
        if employee:
            Crm_Notes.objects.create(
                note_title=note_title,
                note_content=note_content,
                employee=employee  # Link the note to the employee
            )
            create_log("Note Has Been Created", request.user)
        return redirect('create_notes')

    # Check if the user is a superuser
    if request.user.is_superuser:
        notes = Crm_Notes.objects.all()  # Superuser sees all notes
    else:
        # Filter notes for the specific employee
        employee = Employee.objects.filter(user=request.user).first()
        if employee:
            notes = Crm_Notes.objects.filter(employee=employee)
        else:
            notes = Crm_Notes.objects.none()  # No employee, no notes

    context = {
        'notes': notes,
    }

    return render(request, "crm/Notes.html", context)



#? ----------------------------------------------------------------------------------------------------------------------------
# Delete Note
def delete_note (request , id):
    db=request.session.get('database_path')
    note = Crm_Notes.objects.get(id=id)
    note.delete()
    return redirect ('create_notes')

# -------------
# Calendar Setup
def calendar_setup(request):
    events = Event.objects.all()
    event_data = [{
        'id': event.id,
        'title': event.title,
        'start': event.start_date.strftime('%Y-%m-%d'),
        'end': event.end_date.strftime('%Y-%m-%d'),
        'description': event.description
    } for event in events]
    return render(request, 'crm/Calender.html', {'events_json': json.dumps(event_data)})



#? ----------------------------------------------------------------------------------------------------------------------------
# Add Event (POST)
@require_POST
def add_event(request):
    data = json.loads(request.body)
    event = Event.objects.create(
        title=data['title'],
        start_date=data['start'],
        end_date=data['end'],
        description=data['description']
    )
    return JsonResponse({'status': 'success', 'id': event.id})



#? ----------------------------------------------------------------------------------------------------------------------------
# Update Event (POST)
@require_POST
def update_event(request, event_id):
    data = json.loads(request.body)
    event = Event.objects.get(id=event_id)
    event.title = data['title']
    event.start_date = data['start']
    event.end_date = data['end']
    event.description = data['description']
    event.save()
    return JsonResponse({'status': 'success'})



#? ----------------------------------------------------------------------------------------------------------------------------
# Delete Event (POST)
@require_POST
def delete_event(request, event_id):
    Event.objects.filter(id=event_id).delete()
    return JsonResponse({'status': 'success'})



#? ----------------------------------------------------------------------------------------------------------------------------
# Blog View (for Users)
@login_required
def blog_view(request):
    # Get page number from request, default to 1
    page = request.GET.get('page', 1)
    posts_per_page = 3
    
    # Get all blog posts ordered by creation date
    blog_posts = BlogPost.objects.all().order_by('-created_at')
    
    # Set up pagination
    paginator = Paginator(blog_posts, posts_per_page)
    
    try:
        current_posts = paginator.page(page)
    except PageNotAnInteger:
        current_posts = paginator.page(1)
    except EmptyPage:
        current_posts = paginator.page(paginator.num_pages)
    
    # Convert posts to JSON for JavaScript
    posts_data = [{
        'id': post.id,
        'title': post.title,
        'description': post.content[:200] + '...' if len(post.content) > 200 else post.content,
        'category': post.category,
        'date': post.created_at.isoformat(),  # Convert datetime to ISO format string
        'image': post.image.url if post.image else 'https://placehold.co/800x600/png',
    } for post in current_posts]
    
    # Serialize the data
    posts_json = json.dumps(posts_data, cls=DjangoJSONEncoder)
    
    context = {
        'posts_json': posts_json,  # Send serialized JSON
        'total_pages': paginator.num_pages,
        'current_page': int(page),
    }
    
    return render(request, 'Users/Blogs.html', context)






#? ----------------------------------------------------------------------------------------------------------------------------
# Blog Deteiled View (for Users)
def blog_detail_view(request, post_id):
    blog = get_object_or_404(BlogPost, id=post_id)
    tags = blog.tags.all() if hasattr(blog, 'tags') else []
    
    context = {
        'blog': blog,
        'tags': tags,
    }
    
    return render(request, 'Users/BlogDetailedView.html', context)