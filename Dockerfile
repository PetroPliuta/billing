FROM ubuntu:18.04

ENV container=docker LC_ALL=C

#Prepare
RUN \
    #do not ask questions during apt install
    DEBIAN_FRONTEND="noninteractive"; \
    #allow start redis-server, mysql-server
    export RUNLEVEL=5; \
    RUNLEVEL=5; \
    sed -i 's/# deb/deb/g' /etc/apt/sources.list \
    #allow work with services
    && rm -f /usr/sbin/policy-rc.d \
    && dpkg-divert --remove /sbin/initctl \
    && rm -f /sbin/initctl \
    && apt-get update \
    && apt-get install -y apt-utils debconf-utils \
    && echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections \
    && apt-get install -y dialog
#Systemd
RUN apt-get install -y systemd systemd-sysv \
    #fix hostnamectl
    && apt-get install -y dbus \
    #systemd fixes
    && cd /lib/systemd/system/sysinit.target.wants/ \
    && ls | grep -v systemd-tmpfiles-setup | xargs rm -f $1 \
    \
    && rm -f /lib/systemd/system/multi-user.target.wants/* \
    /etc/systemd/system/*.wants/* \
    /lib/systemd/system/local-fs.target.wants/* \
    /lib/systemd/system/sockets.target.wants/*udev* \
    /lib/systemd/system/sockets.target.wants/*initctl* \
    /lib/systemd/system/basic.target.wants/* \
    /lib/systemd/system/anaconda.target.wants/* \
    /lib/systemd/system/plymouth* \
    /lib/systemd/system/systemd-update-utmp* \
    #install useful tools
    && apt-get install -y command-not-found bash-completion ntpdate mc

#deb packets
RUN apt-get -y install nginx freeradius \
    mysql-server libmysqlclient-dev \
    python3-pip python-requests \
    cron logrotate rsyslog \
    && systemctl enable freeradius

# 'echo -e' works
SHELL ["/bin/bash","-c"]

#mysql
RUN service mysql restart \
    && echo -e "create database billing character set utf8 COLLATE utf8_general_ci; \
    CREATE USER 'django'@'%' IDENTIFIED BY 'password'; \
    GRANT ALL PRIVILEGES ON billing.* TO 'django'@'%'; \
    FLUSH PRIVILEGES; " | mysql

#billing
WORKDIR /var/www/billing
COPY . /var/www/billing
COPY docker/cron.d/billing /etc/cron.d/
COPY docker/logrotate.d/* /etc/logrotate.d/
RUN apt -y install pkg-config libdbus-1-dev libglib2.0-dev \
    && pip3 install -r requirements.txt \
    && service mysql restart \
    && python3 manage.py makemigrations \
    && python3 manage.py migrate \
    && echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@billing.com', 'admin')" | python3 manage.py shell \
    && python3 manage.py collectstatic \
    && chmod g-w /etc/cron.d/billing

#web
RUN cp docker/systemd/system/gunicorn.service /etc/systemd/system/ \
    && systemctl enable gunicorn \
    && mkdir /var/log/gunicorn \
    && cp docker/nginx/sites-available/billing /etc/nginx/sites-available/ \
    && ln -sr /etc/nginx/sites-available/billing /etc/nginx/sites-enabled/ \
    && rm -f /etc/nginx/sites-enabled/default
# COPY docker/logrotate.d/gunicorn /etc/logrotate.d/

#freeradius
COPY docker/freeradius/mods-available/billing /etc/freeradius/3.0/mods-available/
COPY docker/freeradius/sites-available/billing /etc/freeradius/3.0/sites-available/
RUN cd /etc/freeradius/3.0/ \
    && ln -sr mods-available/billing mods-enabled/ \
    && ln -sr sites-available/billing sites-enabled/ \
    && mkdir billing \
    && echo '$INCLUDE /var/www/billing/config/radius_clients.conf' >> /etc/freeradius/3.0/clients.conf \
    && touch /var/www/billing/config/radius_clients.conf
COPY docker/freeradius/billing/* /etc/freeradius/3.0/billing/

#clean
RUN unset DEBIAN_FRONTEND \
    && unset RUNLEVEL \
    && echo 'debconf debconf/frontend select Dialog' | debconf-set-selections \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && rm -rf .git docker env frontend node_modules static toolbox .gitignore .dockerignore db.sqlite3 Dockerfile package* webpack.config.js

VOLUME [ "/sys/fs/cgroup" ]

EXPOSE 80 1812/udp 1813/udp

ENTRYPOINT ["/lib/systemd/systemd"]
