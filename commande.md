# installer le package 
pip3 install virtualenv 

#créer votre environement virtuel
virtualenv Django_env
# activer l'environement
source Django_env/bin/activate

# insatll withenoise pour pouvoir servir des fichiers static
pip install whitenoise 

# pour assosier les messages aux alerts bootstrap
pip install django-crispy-forms

# pour collecter tout les fichiers static et les mettre dans un seul dossier
# À executer à chaque fois qu'on modifie les fichiers static
python3 manage.py collectstatic 

# pour installer le package de postgreSQL
pip install psycopg2-binary 

# crée une fichier de dépendances de packages python pour le deployement
python3 -m pip freeze > requirements.txt 

# pour lancer le server en local
python3 manage.py runserver

# pour les modifications côté base de donnée
python3 manage.py makemigrations
python3 manage.py migrate

# pour créer un compte admin
python3 manage.py createsuperuser