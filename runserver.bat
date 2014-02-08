@echo off
set DJANGO_SETTINGS_MODULE=settings.demo
cd src
python manage.py runserver
cd ..

