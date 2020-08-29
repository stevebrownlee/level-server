from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from levelupapi.models import *
from levelupapi.views import register_user, login_user
from levelupapi.views import Games, GameTypes

# pylint: disable=invalid-name
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', Games, 'game')
router.register(r'gametypes', GameTypes, 'gametype')
# router.register(r'gamers', ParkAreas, 'parkarea')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-token-auth', obtain_auth_token),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
