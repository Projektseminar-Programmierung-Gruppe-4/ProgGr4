# Insite Forum - Prog Gr 4

Dieses Forum wurde im Zuge des Moduls Projektseminar Programmieren erstellt.

Ersteller: <br>
-76737 Tim Konle <br>
-76405 Patrick Haag <br>
-76029 Lukas Munz <br>
-76071 Maximilian Baum <br>
-76817 Christian Klingler

## Installation

### 1. öffnen des Projekts im Texteditor (e.g. VS-Code)

### 2. django und psycopg2 installieren (nur wenn nicht vorhanden)

Installation über pip:

pip(3) install django
python(3) -m pip install psycopg2-binary
  
### 3. Aufsetzen einer Postgres Datenbank

-postgreSQL und pgAdmin installieren <br>
-Datenbank informationen in settings.py einbinden (siehe unten)

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

### 5. Projekt migrieren 
-öffne das Terminal des Projekts in VS-Code <br>
-makemigrations mit: python3 manage.py makemigrations <br>
-migrate mit: python3 manage.py migrate

### 6. Superuser erstellen um Admin zu generieren
python3 manage.py createsuperuser

### 7. run server
python3 manage.py runserver

### 8. Applikation im Browser öffnen
URL: localhost:8000

### 9. Login als Admin User
Log In als Admin:
<img width="1429" alt="Bildschirmfoto 2022-01-11 um 13 27 08" src="https://user-images.githubusercontent.com/75367399/148942710-d62e6621-8424-403a-98e6-723996b7b4d8.png">

### 10. Abteilungen hinzufügen
Abteilungen über die Adminpage erstellen:
<img width="1429" alt="Bildschirmfoto 2022-01-11 um 13 27 29" src="https://user-images.githubusercontent.com/75367399/148942796-93ab1050-bbc8-4db8-97ef-ab423185a79c.png">
<img width="1429" alt="Bildschirmfoto 2022-01-11 um 13 27 50" src="https://user-images.githubusercontent.com/75367399/148942846-ab68b628-a058-4fe8-adfb-9889d878fd01.png">

### Das Forum ist erfolgreich eingerichtet und kann von den Mitarbeitern genutzt werden




