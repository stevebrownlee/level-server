from django.urls import path
from .views import *

app_name = "levelupreporting"

urlpatterns = [
    path('reports/usergames', usergame_list, name='usergames'),
    path('reports/eventusers', event_attendee_list, name='eventuser'),
    path('reports/eventsbyhost', event_host_list, name="eventsbyhost")
]
