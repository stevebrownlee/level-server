import sqlite3
from django.shortcuts import render
from levelupapi.models import Event
from levelupreports.views import Connection


def event_host_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                e.date,
                e.time,
                e.id AS event_id,
                g.title AS game_name,
                u.id AS user_id,
                u.first_name || " " || u.last_name AS user_full_name
            FROM levelupapi_event e
            JOIN levelupapi_gamer gr ON e.organizer_id = gr.id
            JOIN auth_user u ON gr.user_id = u.id
            JOIN levelupapi_game g ON e.game_id = g.id
            """)

            dataset = db_cursor.fetchall()
            users_dict = {}

            """
            {
                1: {
                    organizer_id:
                    full_name:
                    events: [
                        {
                            date:
                            time:
                            id:
                            game_name:
                        }
                    ]
                }
            }
            """

            for row in dataset:
                event = Event()
                event.id = row["event_id"]
                event.date = row["date"]
                event.time = row["time"]
                event.game_name = row["game_name"]

                uid = row["user_id"]

                if uid in users_dict:
                    users_dict[uid]['events'].append(event)

                else:
                    users_dict[uid] = {}
                    users_dict[uid]["organizer_id"] = uid
                    users_dict[uid]["full_name"] = row["user_full_name"]
                    users_dict[uid]["events"] = [event]

        list_of_users = users_dict.values()

        template = "users/list_with_events.html"
        context = {
            'event_host_list': list_of_users
        }

        return render(request, template, context)
