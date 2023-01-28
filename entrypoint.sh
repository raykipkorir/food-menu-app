#! /bin/bash
set -e
set -x

python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input

gunicorn -w 2 -b 0.0.0.0:8000 food_menu_project.wsgi
