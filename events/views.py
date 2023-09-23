import datetime
import requests

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView

from common.configs import EVENT_TRIBE_GET_EVENT_API, EVENT_TRIBE_GET_EXTRA, EVENT_TRIBE_TOKEN, GOOGLE_API_KEY
from common.mixins import SuperUserMixin
from events.forms import EventForm
from events.models import Event


class EventDashboardView(SuperUserMixin, View):
    def get(self, request, *args, **kwargs):
        passed_events = Event.objects.filter(end_date__lt=datetime.datetime.utcnow()).count()
        total_events = Event.objects.all().count()
        paid_events = Event.objects.filter(is_free=False).count()
        events = Event.objects.all()
        context = {
            'passed_event_count': passed_events,
            'total_event_count': total_events,
            'paid_event_count': paid_events,
            'events': events
        }

        return render(self.request, template_name='events/dashboard.html', context=context)


class EventDetailView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['KEY'] = GOOGLE_API_KEY
        return context


class EventView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        events_qs = Event.objects.all()[:10]
        if events_qs.exists():
            context['events'] = events_qs
        return render(self.request, template_name='events/events.html', context=context)


class EventCreateView(View):
    @staticmethod
    def is_events_exists(response_data):
        if 'events' not in response_data:
            return False
        return True

    def get_event_data(self, response_data):
        if self.is_events_exists(response_data):
            event_data = response_data.get('events')
            if isinstance(event_data, list) and len(event_data) > 0:
                return event_data[0]
            return None

    @staticmethod
    def get_item_from_event(event_data, item):
        if event_data:
            return event_data.get(item)
        return None

    def get_venue_name_from_event(self, event_data):
        venue_data = self.get_item_from_event(event_data, 'primary_venue')
        if venue_data:
            return venue_data.get('name')
        return None

    def location_details(self, event_data):
        venue_data = self.get_item_from_event(event_data, 'primary_venue')
        if venue_data:
            address = venue_data.get('address')
            if address:
                return address.get('longitude'), address.get('latitude')
        return None, None

    @staticmethod
    def get_is_free_from_event(event_data):
        if 'ticket_availability' in event_data and 'is_free' in event_data:
            if event_data['ticket_availability']['is_free']:
                return event_data['ticket_availability']['is_free']
        return False

    @staticmethod
    def get_price_from_event(event_data):
        if event_data is None:
            return 0.00
        if 'ticket_availability' not in event_data:
            return None
        if 'minimum_ticket_price' not in event_data['ticket_availability']:
            return None
        if 'major_value' not in event_data['ticket_availability']['minimum_ticket_price']:
            return None
        return event_data['ticket_availability']['minimum_ticket_price']['major_value']

    @staticmethod
    def get_image_url(event_data):
        if event_data is None:
            return None
        if 'image' not in event_data:
            return None
        if 'original' not in event_data['image']:
            return None
        if 'url' not in event_data['image']['original']:
            return None
        return event_data['image']['original']['url']

    def get(self, request):
        form = EventForm()
        return render(self.request, 'events/event_add.html', {'form': form})

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            even_tribe_id = form.cleaned_data.get('even_tribe_id')
            api_endpoint = f'{EVENT_TRIBE_GET_EVENT_API}{even_tribe_id}{EVENT_TRIBE_GET_EXTRA}'
            headers = {
                'Authorization': f'Bearer {EVENT_TRIBE_TOKEN}'
            }
            response = requests.get(url=api_endpoint, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                event_data = self.get_event_data(response_data)

                longitude, latitude = self.location_details(event_data)
                link = self.get_item_from_event(event_data, 'url')
                start_date_str = self.get_item_from_event(event_data, "start_date")
                start_time_str = self.get_item_from_event(event_data, "start_time")
                start_date = f'{start_date_str} {start_time_str}'
                end_date_str = self.get_item_from_event(event_data, "end_date")
                end_time_str = self.get_item_from_event(event_data, "end_time")
                end_date = f'{end_date_str} {end_time_str}'
                event = form.save()
                event.name = self.get_item_from_event(event_data, 'name')
                event.longitude = longitude
                event.latitude = latitude
                event.link = link
                event.venue = self.get_venue_name_from_event(event_data)
                event.start_date = start_date
                event.end_date = end_date
                event.ticket_price = self.get_price_from_event(event_data)
                event.is_free = self.get_is_free_from_event(event_data)
                event.image_url = self.get_image_url(event_data)
                event.save()
                return redirect('events:list')
            else:
                messages.debug(f'Cannot get Event Details from Event API status code {response.status_code}')
            return render(self.request, 'events/event_add.html', {'form': form})
