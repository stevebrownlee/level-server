# pylint: disable=missing-module-docstring
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from levelupapi.views import register_user, login_user
from levelupapi.views import Games, GameTypes, Events, Profile

#####################################
##                                 ##
##           Your new              ##
##      request_handler.py         ##
##                                 ##
#####################################


# pylint: disable=invalid-name
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', Games, 'game')
router.register(r'gametypes', GameTypes, 'gametype')
router.register(r'events', Events, 'event')
router.register(r'profile', Profile, 'profile')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
