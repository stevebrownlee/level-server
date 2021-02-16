"""View module for handling requests about park areas"""
from django.core.exceptions import ValidationError
from django.db.models.fields import BooleanField
from django.http import HttpResponseServerError
from django.db.models import Count, Q, When, Case
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from levelupapi.models import Game, Gamer, GameType


class Games(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)

        game = Game()

        try:
            game.title = request.data["title"]
            game.maker = request.data["maker"]
            game.number_of_players = request.data["numberOfPlayers"]
            game.skill_level = request.data["skillLevel"]
            game.user_event_count = 0
            game.event_count = 0

        except KeyError as ex:
            return Response({'message': 'Incorrect key was sent in request'}, status=status.HTTP_400_BAD_REQUEST)

        game.gamer = gamer

        try:
            gametype = GameType.objects.get(pk=request.data["gameTypeId"])
            game.gametype = gametype
        except GameType.DoesNotExist as ex:
            return Response({'message': 'Game type provided is not valid'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)

        try:
            game = Game.objects.annotate(
                event_count=Count('events'),
                user_event_count=Count(
                    'events',
                    filter=Q(events__organizer=gamer)
                )
            ).get(pk=pk)

            serializer = GameSerializer(game, context={'request': request})

            return Response(serializer.data)

        except Game.DoesNotExist as ex:
            return Response({'message': 'Game does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        gamer = Gamer.objects.get(user=request.auth.user)

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.skill_level = request.data["skillLevel"]
        game.gamer = gamer

        gametype = GameType.objects.get(pk=request.data["gameTypeId"])
        game.gametype = gametype
        game.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 204, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        gamer = Gamer.objects.get(user=request.auth.user)

        games = Game.objects.annotate(
            event_count=Count('events'),
            user_event_count=Count(
                'events',
                filter=Q(events__organizer=gamer)
            ),
            owner=Case(
                When(gamer=gamer, then=True),
                default=False,
                output_field=BooleanField()
            )
        )
        print(games.query)

        if "sortBy" in request.query_params:
            attr = request.query_params["sortBy"]
            if attr == "skill":
                games = games.order_by("-skill_level")
            elif attr == "players":
                games = games.order_by("-number_of_players")

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for game creator"""

    class Meta:
        model = Gamer
        fields = ('id',)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""

    gamer = GamerSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'gamer', 'event_count',
                  'number_of_players', 'skill_level', 'gametype',
                  'user_event_count', 'owner',)
        depth = 1


class MinimalGameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""

    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'number_of_players',
                  'skill_level', 'gametype', )
        depth = 1
