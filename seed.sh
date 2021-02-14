#!/bin/bash

rm -rf levelupapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations levelupapi
python manage.py migrate levelupapi
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata gamers
python manage.py loaddata gametypes
python manage.py loaddata games
python manage.py loaddata events

