#!/bin/bash
python manage.py makemigrations db
python manage.py migrate
python manage.py runserver 0.0.0.0:$PORT
