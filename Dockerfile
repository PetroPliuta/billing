FROM ubuntu:18.04
ENV container=docker LC_ALL=C
COPY . /var/www/billing
COPY docker/ /
RUN \
    #do not ask questions during apt-get install
    export DEBIAN_FRONTEND="noninteractive" \
    && sed -i 's/# deb/deb/g' /etc/apt/sources.list \
    #allow work with services
    && rm -f /usr/sbin/policy-rc.d \
    && dpkg-divert --remove /sbin/initctl \
    && rm -f /sbin/initctl \
    && apt-get update \
    && apt-get install -y apt-utils debconf-utils \
    && echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections \
    && apt-get install -y dialog \
    #Systemd
    && apt-get install -y systemd systemd-sysv \
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
    && apt-get install -y command-not-found bash-completion ntpdate mc \
    #deb packets
    && apt-get -y install nginx freeradius \
    mysql-server libmysqlclient-dev \
    python3-pip python-requests \
    cron logrotate rsyslog \
    && systemctl enable freeradius \
    #mysql
    #fix building on dockerhub
    && find /var/lib/mysql -type f -exec touch {} \; \
    #
    && /etc/init.d/mysql restart \
    && echo "create database billing character set utf8 COLLATE utf8_general_ci; \
    CREATE USER 'django'@'%' IDENTIFIED BY 'password'; \
    GRANT ALL PRIVILEGES ON billing.* TO 'django'@'%'; \
    FLUSH PRIVILEGES; " | mysql \
    #billing. for dbus-python
    && apt-get -y install pkg-config libdbus-1-dev libglib2.0-dev \
    #billing
    python-pip \
    && pip2 install requests-unixsocket \
    && cd /var/www/billing \
    && pip3 install -r requirements.txt \
    && python3 -B manage.py makemigrations \
    && python3 -B manage.py migrate \
    && echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
    User.objects.create_superuser('admin', 'admin@billing.com', 'admin')" | python3 -B manage.py shell \
    && python3 -B manage.py collectstatic \
    && sed -i 's/DEBUG = True/DEBUG = False/g' billing/settings.py \
    && chmod 0644 /etc/cron.d/billing \
    && chmod 0644 /etc/logrotate.d/* \
    #web
    && systemctl enable gunicorn \
    && mkdir /var/log/gunicorn \
    && ln -sr /etc/nginx/sites-available/billing /etc/nginx/sites-enabled/ \
    && rm -f /etc/nginx/sites-enabled/default \
    #freeradius
    && cd /etc/freeradius/3.0/ \
    && ln -sr mods-available/billing mods-enabled/ \
    && ln -sr sites-available/billing sites-enabled/ \
    && echo '$INCLUDE /var/www/billing/configuration/radius_clients.conf' >> /etc/freeradius/3.0/clients.conf \
    && touch /var/www/billing/configuration/radius_clients.conf \
    #clean
    && /etc/init.d/mysql stop \
    && unset DEBIAN_FRONTEND \
    && echo 'debconf debconf/frontend select Dialog' | debconf-set-selections \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && cd /var/www/billing \
    && rm -rf .git docker env frontend node_modules static toolbox .gitignore .dockerignore db.sqlite3 Dockerfile package* webpack.config.js \
    && (find -iname __pycache__ -exec rm -rf {} \; || true)
VOLUME [ "/sys/fs/cgroup" ]
EXPOSE 80 1812/udp 1813/udp
ENTRYPOINT ["/lib/systemd/systemd"]
