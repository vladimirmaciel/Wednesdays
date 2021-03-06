from django.shortcuts import redirect, render
import calendar  # imporanto biblioteca calendar do django
# importa HTMLCalendar dentro da bilioteca calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect, response
from django.http import HttpResponse
from .models import Event, Venue
from .forms import VenueForm, EventForm
import csv

# Import PDF Stuff
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Import Pagination Stuff
from django.core.paginator import Paginator


#  Generate a PDF file venue List
#  instalar biblioteca reportlab (pip install reportlab)


def venue_pdf(request):
    # Create Bytesteam buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Add some lines of text
    # lines = [
    #     "This is line 1",
    #     "This is line 2",
    #     "This is line 3",
    # ]

    # Designate The Model
    venues = Venue.objects.all()

    # Create blank list
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")

    # Loop
    for line in lines:
        textob.textLine(line)

    # Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return something
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')


# Generate csv File Venue List


def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # Create csv writer
    writer = csv.writer(response)

    # Designate The Model
    venues = Venue.objects.all()

    #  Add Column headings to the csv file
    writer.writerow(['Venue Name', 'Address', 'Zip Code',
                    'Phone', 'Web Address', 'Email'])

    # Loop Thu and output
    for venue in venues:

        writer.writerow(
            [venue.name,
             venue.address,
             venue.zip_code,
             venue.phone,
             venue.web,
             venue.email_address])

    return response

# Generate Text File Venue List


def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    # Designate The Model
    venues = Venue.objects.all()

    # Create blank list
    lines = []

    # Loop Thu an output
    for venue in venues:
        # lines.append(f'{venue}\n') lista todos
        lines.append(
            f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n\n')

        # lines = ["This is line 1\n",
        #          "This is line 2\n",
        #          "This is line 3\n\n",
        #          "Vladimir Maciel Serra is Awesome!\n"
        #          ]

        # Write To TextFile
    response.writelines(lines)
    return response

# Delete Venue


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')

# Delete an Event


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    # messages.success(request, ("Event Deleted!!"))
    return redirect('list-events')


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)  # passado o id do objeto desejado
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'events/update_event.html', {'event': event, 'form': form})


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                # form.save()
                event = form.save(commit=False)
                # event.manager = request.user # logged in user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        # Just Going To The Page, Not Submitting
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


# def update_event(request, event_id):
#     event = Event.objects.get(pk=event_id) # passado o id do objeto desejado
#     form = EventForm(request.POST or None, instance=event)
#     if form.is_valid():
#         form.save()
#         return redirect('list-events')
#     return render(request, 'events/update_events.html',{'event':event, 'form':form})


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)  # passado o id do objeto desejado
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'events/update_venue.html', {'venue': venue, 'form': form})


def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)

        return render(request, 'events/search_venues.html', {'searched': searched, 'venues': venues})
    else:
        return render(request, 'events/search_venues.html', {})


def show_venue(request, venue_id):  # <venue_id> foi passado como parametro
    # utilizamo o id para mostras o detalhes de cada campo
    venue = Venue.objects.get(pk=venue_id)  # passado o id do objeto desejado
    return render(request, 'events/show_venue.html', {'venue': venue})


def list_venues(request):
    #venue_list = Venue.objects.all().order_by('?')
    venue_list = Venue.objects.all()

    # Set up Pagination
    p = Paginator(Venue.objects.all(), 3)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages
    return render(request, 'events/venue.html',
                  {'venue_list': venue_list,
                   'venues': venues,
                   'nums': nums}
                  )


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        # passa o VenueForm para variavel form
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    # Declara uma variavel form com nome form
    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})


def all_events(request):
    '''
        Esta view ir?? lsitar todos do eventos cadastrados 
    '''
    # event_list = Event.objects.all()
    event_list = Event.objects.all().order_by('event_date')
    return render(request, 'events/event_list.html', {'event_list': event_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Vladimir"
    # capitalize method returns a string where the first character is upper case, and the rest is lower case.
    month = month.capitalize()

    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # Traz o ano atual
    now = datetime.now()
    current_year = now.year

    # Traz a hora atual
    time = now.strftime("%H:%M:%S %p")

    return render(request,
                  # o arquivo home.html encontra-se dentro da pastas envents em templates
                  'events/home.html', {
                      "first_name": name,  # declarei uma variavel first_name que vai ser utilizada  no home.html
                      "year": year,
                      "month": month,
                      "month_number": month_number,
                      "cal": cal,
                      "current_year": current_year,
                      "time": time,


                  })  # redireciona para  a pasta events/templates arquivo home.html
