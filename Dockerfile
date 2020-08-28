# FROM django:onbuild
FROM python:latest

WORKDIR /var/www
COPY . /var/www

RUN apt update && apt -y install nodejs npm
RUN npm install
RUN npm run build
RUN pip install -r requirements.txt

ENTRYPOINT python manage.py runserver 0.0.0.0:8000
