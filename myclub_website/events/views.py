from django.shortcuts import redirect, render
import calendar # imporanto biblioteca calendar do django
from calendar import HTMLCalendar # importa HTMLCalendar dentro da bilioteca calendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue
from .forms import VenueForm, EventForm



def add_event(request):
	submitted = False
	if request.method == "POST":
		if request.user.is_superuser:
			form = EventFormAdmin(request.POST)
			if form.is_valid():
					form.save()
					return 	HttpResponseRedirect('/add_event?submitted=True')	
		else:
			form = EventForm(request.POST)
			if form.is_valid():
				#form.save()
				event = form.save(commit=False)
				# event.manager = request.user # logged in user
				event.save()
				return 	HttpResponseRedirect('/add_event?submitted=True')	
	else:
		# Just Going To The Page, Not Submitting 
		if request.user.is_superuser:
			form = EventFormAdmin
		else:
			form = EventForm

		if 'submitted' in request.GET:
			submitted = True

	return render(request, 'events/add_event.html', {'form':form, 'submitted':submitted})



# def update_event(request, event_id):
#     event = Event.objects.get(pk=event_id) # passado o id do objeto desejado
#     form = EventForm(request.POST or None, instance=event)
#     if form.is_valid():
#         form.save()
#         return redirect('list-events')
#     return render(request, 'events/update_events.html',{'event':event, 'form':form})


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id) # passado o id do objeto desejado
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'events/update_venue.html',{'venue':venue, 'form':form})


def search_venues(request):
    if request.method == "POST":
         searched = request.POST['searched']
         venues = Venue.objects.filter(name__contains=searched)
         
         return render(request, 'events/search_venues.html',{'searched':searched, 'venues':venues})
    else:
         return render(request, 'events/search_venues.html',{})
        


def show_venue(request, venue_id): # <venue_id> foi passado como parametro
    # utilizamo o id para mostras o detalhes de cada campo 
    venue = Venue.objects.get(pk=venue_id) # passado o id do objeto desejado
    return render(request, 'events/show_venue.html',{'venue':venue})


def list_venues(request):
    '''
        Esta view irá lsitar todas as veunes cadastrados 
    '''
    # venue_list = Venue .objects.all()
    venue_list = Venue.objects.all()
    return render(request, 'events/venue.html',{'venue_list':venue_list})

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        #passa o VenueForm para variavel form 
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
            
        
    # Declara uma variavel form com nome form 
    return render(request, 'events/add_venue.html',{'form':form, 'submitted':submitted})


def all_events(request):
    '''
        Esta view irá lsitar todos do eventos cadastrados 
    '''
    # event_list = Event.objects.all()
    event_list = Event.objects.all().order_by('event_date')
    return render(request, 'events/event_list.html',{'event_list':event_list})



def home(request, year = datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Vladimir"
    month = month.capitalize() # capitalize method returns a string where the first character is upper case, and the rest is lower case.
    
    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    
    # create a calendar 
    cal = HTMLCalendar().formatmonth(year,month_number)
    
    # Traz o ano atual
    now =  datetime.now()
    current_year = now.year
    
    # Traz a hora atual
    time = now.strftime("%H:%M:%S %p")
    
    
    return render(request,
                  # o arquivo home.html encontra-se dentro da pastas envents em templates
                  'events/home.html',{
                  "first_name":name, # declarei uma variavel first_name que vai ser utilizada  no home.html
                  "year":year,
                  "month":month,
                  "month_number":month_number,
                  "cal":cal,
                  "current_year":current_year,
                  "time":time,
        
        
        }) # redireciona para  a pasta events/templates arquivo home.html