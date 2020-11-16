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
;



SELECT
    e.id as event_id,
    e.date,
    e.time,
    g.title as game_name,
    u.id AS signed_up_gamer_id,
    u.first_name || " " || u.last_name as user_full_name
FROM levelupapi_event e
JOIN levelupapi_eventgamers eg ON e.id = eg.event_id
JOIN levelupapi_gamer gr ON eg.gamer_id = gr.id
JOIN auth_user u ON gr.user_id = u.id
JOIN levelupapi_game g ON e.game_id = g.id
;