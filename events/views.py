from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue, University, User, MyClubUser
from .forms import VenueForm, EventForm
from django.contrib import messages
from django.http import HttpResponse
from django.http import FileResponse


# імпорт для пдф файлів
# from django.http import FileResponse
# import io
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter


# home page у форматі календаря
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "dear visitors our IT club"
    month = month.capitalize()
    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calendar
    cal = HTMLCalendar().formatmonth(
        year,
        month_number)
    # Get current year
    now = datetime.now()
    current_year = now.year

    # Query the Events Model For Dates
    # event_list = Event.objects.filter(
    # event_date__year=year,
    # event_date__month=month_number
    # )

    # Get current time
    time = now.strftime('%H:%M %p')
    return render(request,
                  'events/home.html', {
                      "name": name,
                      "year": year,
                      "month": month,
                      "month_number": month_number,
                      "cal": cal,
                      "current_year": current_year,
                      "time": time,
                      # "event_list": event_list,
                  })


# дивимося список подій, реалізація за допомогою витягування всіх атрибутів у моделі Event
def all_events(request):
    event_list = Event.objects.all().order_by('event_date')
    return render(request, 'events/event_list.html', {'event_list': event_list})


# аналогічно "витягуємо" всі об'єкти прописані у моделі, рендеримо список місць проведення
def list_venues(request):
    venue_list = Venue.objects.all()
    return render(request, 'events/venue.html',
                  {'venue_list': venue_list})


# отримати з бази даних місця проведення заходів за іd номером в БД
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)  # get - отримати передивитися через список місць проведення
    return render(request, 'events/show_venue.html',
                  {'venue': venue})


# реалізація пошукового вікна "Search" для місць проведення
def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html',
                      {'searched': searched, 'venues': venues})
    else:
        return render(request, 'events/search_venues.html', {})


# додаємо нові IT івенти
def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


#  оновлюємо IT івенти
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')  # name в path

    return render(request, 'events/update_event.html',
                  {'event': event,  # значенням ключа event буде змінна event
                   'form': form})


# видаляємо дані якщо юзер є менеджером івенту
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, ("Event Deleted!!"))
        return redirect('list-events')
    else:
        messages.success(request, ("You Aren't Authorized To Delete This Event!"))
        return redirect('list-events')


# зповнюємо форму для нового місця проведення івенту
def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})


#  аналогічно методу в івенті робимо оновлення для місць проведення події
def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')

    return render(request, 'events/update_venue.html',
                  {'venue': venue,  # значенням ключа venue буде змінна venue
                   'form': form})


# видалення місця проведення
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')


# IT University
def info_univer(request):
    info_list = University.objects.get
    return render(request, 'events/info_list.html',
                  {'info_list': info_list})
