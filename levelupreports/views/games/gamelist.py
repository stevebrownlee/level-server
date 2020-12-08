"""HTML report"""
import sqlite3
from django.http import HttpResponse
from rest_framework import status

from django.shortcuts import render
from levelupapi.models import Event
from levelupreports.views import Connection


def get_game_list(request):
    """Respond with HTML report of all games"""
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                g.title,
                g.maker,
                g.number_of_players,
                gt.label
            FROM levelupapi_game g
            JOIN levelupapi_gametype gt ON g.gametype_id = gt.id
            """)

            dataset = db_cursor.fetchall()

        template = "games/list.html"
        context = {
            'all_available_games_list': dataset
        }

        return render(request, template, context)
    else:

        return HttpResponse(
            None,
            content_type='text/plain',
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
