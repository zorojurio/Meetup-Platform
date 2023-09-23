from django.urls import path, include

from events.views import EventView, EventCreateView, EventDetailView, EventDashboardView

app_name = "events"
urlpatterns = [
    path('', EventView.as_view(), name='list'),
    path('create', EventCreateView.as_view(), name='create'),
    path('<int:pk>', EventDetailView.as_view(), name='detail'),
    path('dashboard', EventDashboardView.as_view(), name='dashboard')
]
