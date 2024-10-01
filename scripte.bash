#!/bin/bash
# deploy to vercel
pip install django

pip install whitenoise 

pip install django_use_email_as_username

pip install whitenoise

python3 -m pip freeze > requirements.txt 

python3 manage.py runserver
