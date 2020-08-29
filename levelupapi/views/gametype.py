"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import GameType


class GameTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = GameType
        url = serializers.HyperlinkedIdentityField(
            view_name='gametype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'label')


class GameTypes(ViewSet):
    """Level up games"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            game_type = GameType.objects.get(pk=pk)
            serializer = GameTypeSerializer(game_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to park attractions resource

        Returns:
            Response -- JSON serialized list of park attractions
        """
        gametypes = GameType.objects.all()

        serializer = GameTypeSerializer(
            gametypes, many=True, context={'request': request})
        return Response(serializer.data)
