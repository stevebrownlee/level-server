import sqlite3
from django.shortcuts import render
from levelupapi.models import Game
from levelupreports.views import Connection


def usergame_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    g.id,
                    g.title,
                    g.maker,
                    g.gametype_id,
                    g.number_of_players,
                    g.skill_level,
                    u.id user_id,
                    u.first_name || ' ' || u.last_name AS full_name
                FROM
                    levelupapi_game g
                JOIN
                    levelupapi_gamer gr ON g.gamer_id = gr.id
                JOIN
                    auth_user u ON gr.user_id = u.id
            """)

            dataset = db_cursor.fetchall()
            gamers_dict = {}

            for row in dataset:
                game = Game()
                game.title = row["title"]
                game.maker = row["maker"]
                game.skill_level = row["skill_level"]
                game.number_of_players = row["number_of_players"]
                game.gametype_id = row["gametype_id"]

                uid = row["user_id"]
                if uid in gamers_dict:
                    gamers_dict[uid]['games'].append(game)
                else:
                    gamers_dict[uid] = {}
                    gamers_dict[uid]["id"] = uid
                    gamers_dict[uid]["full_name"] = row["full_name"]
                    gamers_dict[uid]["games"] = [game]

        # Get only the values from the dictionary and create a list from them
        list_of_user_objects = gamers_dict.values()

        # Specify the HTML template and provide data context
        template = 'users/list_with_games.html'
        context = {
            'usergame_list': list_of_user_objects
        }

        return render(request, template, context)