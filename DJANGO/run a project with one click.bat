@echo off
start cmd /k "cd /d C:\Arkboss\venv\scripts & activate & cd /d C:\Arkboss\src\arkboss & python manage.py runserver"
Ping -n 20 localhost
start C:\"Program Files (x86)"\Google\Chrome\Application\chrome.exe "http://127.0.0.1:8000/"
