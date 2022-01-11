# Insite Forum - Prog Gr 4

Dieses Forum wurde im Zuge des Moduls Projekt Programmierung erstellt.

## Installation

### 1. open Project in Texteditor (e.g. VS-Code)

### 2. install django (nur wenn nicht vorhanden)

Installation über pip:

pip3 install django
  
### 3. Aufsetzen einer Postgres Datenbank

### 4. Einbindung der der Datenbank in Django
Einbinden der Datenbank über die Settings.py

```python
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'databsename' ,
        'USER' : 'username' ,
        'PASSWORD' : 'password',
        'HOST' : 'localhost' ,
        'PORT' : '5432'
    }
}
````

### 5. migrate project
-open Terminal for the project in VS-Code <br>
-makemigrations with: python3 manage.py makemigrations <br>
-migrate with: python3 manage.py migrate

### 6. create superuser to get an Admin
python3 manage.py createsuperuser

### 7. run server
python3 manage.py runserver

### 8. open browser
URL: localhost:8000

### 9. login with admin user
<img width="1429" alt="Bildschirmfoto 2022-01-11 um 13 27 08" src="https://user-images.githubusercontent.com/75367399/148942710-d62e6621-8424-403a-98e6-723996b7b4d8.png">

### 10. Abteilungen hinzufügen
<img width="1429" alt="Bildschirmfoto 2022-01-11 um 13 27 29" src="https://user-images.githubusercontent.com/75367399/148942796-93ab1050-bbc8-4db8-97ef-ab423185a79c.png">
<img width="1429" alt="Bildschirmfoto 2022-01-11 um 13 27 50" src="https://user-images.githubusercontent.com/75367399/148942846-ab68b628-a058-4fe8-adfb-9889d878fd01.png">

### Ready to use the Forum!!!


## How to use the insite-Forum:
