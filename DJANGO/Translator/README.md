# Steps to Follow
1: Install required packages
2: Set the values as given in the file settings.py
3: Add `{% load i18n %}` in all pages that may require translation
4: Enclose every static content with `{% trans '' %}`
    eg: `{% trans 'Home' %}`
5: Run `django-admin makemessages -l ml` command in terminal
    above `ml` stands for Malayalam
6: A file will be added to the directory mentioned in settings `LOCALE_PATHS`
    `locale/ml/LC_MESSAGES/django.po`
7: All static strings that are enclosed with `{% trans '' %}` will be listed there with space to fill in its translation to language mentioned in the terminal command
    Fill in the translated content at designated areas
8: Run `django-admin compilemessages` command in terminal
