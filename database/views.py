from django.shortcuts import render , redirect , get_object_or_404
from .models import Crm_Contacts , Crm_Notes , Event
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json





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
        return redirect('create_contact')    
    # For GET request, render the form and table
    contacts = Crm_Contacts.objects.all()  # Fetch all contacts to display in the table
    return render(request, "crm/Contacts.html", {'contacts': contacts})


def delete (request , id):
    db=request.session.get('database_path')
    contact = Crm_Contacts.objects.get(id=id)
    contact.delete()
    return redirect ('create_contact')




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

        contact.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    


def create_notes(request):
    if request.method == "POST":
      note_title = request.POST.get('note_title')
      note_content = request.POST.get('note_content')
      Crm_Notes.objects.create(
          note_title = note_title,
          note_content = note_content
      )
      return redirect ('create_notes')

    notes = Crm_Notes.objects.all()
    return render(request, "crm/Notes.html" , {'notes' : notes,})

def delete_note (request , id):
    db=request.session.get('database_path')
    note = Crm_Notes.objects.get(id=id)
    note.delete()
    return redirect ('create_notes')




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

@require_POST
def delete_event(request, event_id):
    Event.objects.filter(id=event_id).delete()
    return JsonResponse({'status': 'success'})