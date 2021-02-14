SELECT e.date,
    e.time,
    e.id AS event_id,
    g.title AS game_name,
    u.id AS user_id,
    u.first_name || " " || u.last_name AS user_full_name
FROM levelupapi_event e
    JOIN levelupapi_gamer gr ON e.organizer_id = gr.id
    JOIN auth_user u ON gr.user_id = u.id
    JOIN levelupapi_game g ON e.game_id = g.id;
CREATE VIEW USER_EVENTS AS
SELECT e.id as event_id,
    e.date,
    e.time,
    g.title as game_name,
    u.id AS signed_up_gamer_id,
    u.first_name || " " || u.last_name as user_full_name
FROM levelupapi_event e
    JOIN levelupapi_eventgamers eg ON e.id = eg.event_id
    JOIN levelupapi_gamer gr ON eg.gamer_id = gr.id
    JOIN auth_user u ON gr.user_id = u.id
    JOIN levelupapi_game g ON e.game_id = g.id;
SELECT *
FROM USER_EVENTS;
CREATE VIEW USER_EVENT_COUNT AS
SELECT COUNT(e.id) events,
    u.id AS signed_up_gamer_id,
    u.first_name || " " || u.last_name as user_full_name
FROM levelupapi_event e
    JOIN levelupapi_eventgamers eg ON e.id = eg.event_id
    JOIN levelupapi_gamer gr ON eg.gamer_id = gr.id
    JOIN auth_user u ON gr.user_id = u.id
GROUP BY signed_up_gamer_id,
    user_full_name;
SELECT events,
    signed_up_gamer_id,
    user_full_name
FROM USER_EVENT_COUNT;
-- Get all events with number of attendees and if current user is an attendee
SELECT "levelupapi_event"."id",
    "levelupapi_event"."game_id",
    "levelupapi_event"."organizer_id",
    "levelupapi_event"."description",
    "levelupapi_event"."date",
    "levelupapi_event"."time",
    COUNT("levelupapi_eventgamers"."id") AS "attendees",
    COUNT(
        CASE
            WHEN "levelupapi_eventgamers"."gamer_id" = 1 THEN "levelupapi_eventgamers"."id"
            ELSE NULL
        END
    ) AS "joined"
FROM "levelupapi_event"
    LEFT OUTER JOIN "levelupapi_eventgamers" ON (
        "levelupapi_event"."id" = "levelupapi_eventgamers"."event_id"
    )
GROUP BY "levelupapi_event"."id",
    "levelupapi_event"."game_id",
    "levelupapi_event"."organizer_id",
    "levelupapi_event"."description",
    "levelupapi_event"."date",
    "levelupapi_event"."time";
SELECT "levelupapi_event"."id",
    "levelupapi_event"."game_id",
    "levelupapi_event"."organizer_id",
    "levelupapi_event"."description",
    "levelupapi_event"."date",
    "levelupapi_event"."time",
    COUNT("levelupapi_eventgamers"."id") AS "attendees",
    COUNT(
        CASE
            WHEN "levelupapi_eventgamers"."gamer_id" = 1 THEN "levelupapi_eventgamers"."id"
            ELSE NULL
        END
    ) AS "joined"
FROM "levelupapi_event"
    LEFT OUTER JOIN "levelupapi_eventgamers" ON (
        "levelupapi_event"."id" = "levelupapi_eventgamers"."event_id"
    )
GROUP BY "levelupapi_event"."id",
    "levelupapi_event"."game_id",
    "levelupapi_event"."organizer_id",
    "levelupapi_event"."description",
    "levelupapi_event"."date",
    "levelupapi_event"."time"
;


SELECT "levelupapi_game"."id",
    "levelupapi_game"."gametype_id",
    "levelupapi_game"."title",
    "levelupapi_game"."maker",
    "levelupapi_game"."gamer_id",
    "levelupapi_game"."number_of_players",
    "levelupapi_game"."skill_level",
    COUNT("levelupapi_event"."id") AS "event_count",
    COUNT(
        CASE
            WHEN "levelupapi_event"."organizer_id" = 1 THEN "levelupapi_event"."id"
            ELSE NULL
        END
    ) AS "user_event_count",
    CASE
        WHEN "levelupapi_game"."gamer_id" = 1 THEN True
        ELSE False
    END AS "owner"
FROM "levelupapi_game"
    LEFT OUTER JOIN "levelupapi_event" ON (
        "levelupapi_game"."id" = "levelupapi_event"."game_id"
    )
GROUP BY "levelupapi_game"."id",
    "levelupapi_game"."gametype_id",
    "levelupapi_game"."title",
    "levelupapi_game"."maker",
    "levelupapi_game"."gamer_id",
    "levelupapi_game"."number_of_players",
    "levelupapi_game"."skill_level",
    CASE
        WHEN "levelupapi_game"."gamer_id" = 1 THEN True
        ELSE False
    END
;