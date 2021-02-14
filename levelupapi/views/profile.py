"""View module for handling requests about park areas"""
from django.contrib.auth.models import User
from django.db.models import Count, Q, Case, When
from django.db.models.fields import BooleanField
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Event, Gamer, EventGamers, Game


class Profile(ViewSet):
    """Gamer can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info and events
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.annotate(
            owner=Case(
                When(organizer=gamer, then=True),
                default=False,
                output_field=BooleanField()
            )
        ).filter(
            Q(registrations__gamer=gamer) |
            Q(organizer=gamer)
        )

        events = EventSerializer(
            events, many=True, context={'request': request})
        gamer = GamerSerializer(
            gamer, many=False, context={'request': request})

        profile = {}
        profile["gamer"] = gamer.data
        profile["events"] = events.data

        return Response(profile)

    @action(methods=['get', 'post', 'delete'], detail=True)
    def signup(self, request, pk=None):
        """Managing gamers signing up for events"""

        if request.method == "POST":
            event = Event.objects.get(pk=pk)
            gamer = Gamer.objects.get(user=request.auth.user)

            try:
                registration = EventGamers.objects.get(
                    event=event, gamer=gamer)
                return Response(
                    {'message': 'Gamer already signed up this event.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except EventGamers.DoesNotExist:
                registration = EventGamers()
                registration.event = event
                registration.gamer = gamer
                registration.save()

                return Response({}, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            try:
                event = Event.objects.get(pk=pk)
            except Event.DoesNotExist:
                return Response(
                    {'message': 'Event does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            gamer = Gamer.objects.get(user=request.auth.user)

            try:
                registration = EventGamers.objects.get(
                    event=event, gamer=gamer)
                registration.delete()
            except EventGamers.DoesNotExist:
                return Response(
                    {'message': 'Not currently registered for event.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""

    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'gamer',
                  'number_of_players', 'skill_level', 'gametype')


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = UserSerializer(many=False)
    games = GameSerializer(many=True)

    class Meta:
        model = Gamer
        fields = ('user', 'bio', 'games',)


class EventSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for events"""
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        url = serializers.HyperlinkedIdentityField(
            view_name='event',
            lookup_field='id'
        )
        fields = ('id', 'url', 'game', 'description', 'date', 'time', 'owner',)
