from levelupreports.views.users.eventsbyuser import event_host_list
import sqlite3
from django.shortcuts import render
from levelupapi.models import Event, Gamer
from levelupreports.views import Connection

def event_attendee_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                e.id as event_id,
                e.date,
                e.time,
                g.title as game_name,
                u.id AS user_id,
                u.first_name || " " || u.last_name as user_full_name
            FROM levelupapi_event e
            JOIN levelupapi_eventgamer eg ON e.id = eg.event_id
            JOIN levelupapi_gamer gr ON eg.gamer_id = gr.id
            JOIN auth_user u ON gr.user_id = u.id
            JOIN levelupapi_game g ON e.game_id = g.id
            """)

            dataset = db_cursor.fetchall()
            events_dict = {}

            """
            {
                1: {
                    date:
                    time:
                    game_name:
                    attendees: [
                        {
                            gamer_id: 1
                            full_name: "steve brownlee"
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

                attendee_dict = {}

                attendee_dict.user_id = row["user_id"]
                attendee_dict.full_name = row["user_full_name"]

                if event.id in events_dict:
                    events_dict[event.id]["attendees"].append(attendee_dict)

                else:
                    events_dict[event.id] = {}
                    events_dict[event.id]["date"] = event.date
                    events_dict[event.id]["time"] = event.time
                    events_dict[event.id]["game_name"] = event.game_name
                    events_dict[event.id]["attendees"] = [attendee_dict]

        event_list = events_dict.values()

        template = "events/list_with_attendees.html"
        context = {
            'event_attendee_list': event_list
        }

        return render(request, template, context)
