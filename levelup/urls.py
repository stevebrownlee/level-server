# pylint: disable=missing-module-docstring
from django.conf.urls import include
from django.urls import path, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from rest_framework import permissions
from levelupapi.views import register_user, login_user
from levelupapi.views import Games, GameTypes, Events, Profile

schema_view = get_schema_view(
    openapi.Info(
        title="LevelUp API",
        default_version='v1',
        description="API for creating games and events",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@levelup.local"),
        license=openapi.License(name="BSD License"),
    ),

    public=True,
    permission_classes=[permissions.AllowAny],
)

# pylint: disable=invalid-name
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', Games, 'game')
router.register(r'gametypes', GameTypes, 'gametype')
router.register(r'events', Events, 'event')
router.register(r'profile', Profile, 'profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    path('', include('levelupreports.urls')),
]
