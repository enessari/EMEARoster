#!/usr/bin/env bash
python manage.py makemigrations
python manage.py migrate
nohup /bin/sh  BackgroundTask/task_runner/background_task.sh &
gunicorn EMEARoster.wsgi --workers 2