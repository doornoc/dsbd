#!/bin/bash

/usr/sbin/nginx -g "daemon off;" &

#python manage.py migrate
gunicorn --bind 0.0.0.0:8000 -w 2 dsbd.wsgi:application &

#
daphne -b 0.0.0.0 -p 8001 dsbd.asgi:application