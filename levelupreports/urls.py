from django.urls import path
from .views import *

app_name = "levelupreporting"

urlpatterns = [
    path('reports/usergames', usergame_list, name='home'),
]
