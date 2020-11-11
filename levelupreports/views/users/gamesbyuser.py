import sqlite3
from django.shortcuts import render
from levelupapi.models import Game, Gamer
from ..connection import Connection


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
                INNER JOIN
                    levelupapi_gamer gr
                    ON g.gamer_id = gr.id
                INNER JOIN
                    auth_user u
                    ON gr.user_id = u.id
            """)

            all_user_games = []
            dataset = db_cursor.fetchall()

            """
            {
                1: {
                    "full_name": "kcfcmfk",
                    "id": 1,
                    "games": [
                        {
                            "id": 1,
                            "title": "jvioevnofkd"
                        }
                    ]
                }
            }
            """

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


        json_response = gamers_dict.values()


        template = 'users/list_with_games.html'
        context = {
            'usergame_list': json_response
        }

        return render(request, template, context)