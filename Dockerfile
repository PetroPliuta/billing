# FROM django:onbuild
FROM python:latest
 
WORKDIR /var/www
COPY . /var/www

RUN pip install -r requirements.txt

ENTRYPOINT python manage.py runserver
