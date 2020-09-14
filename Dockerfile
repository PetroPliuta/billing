FROM ubuntu:18.04

ENV container=docker LC_ALL=C

RUN \
    #do not ask questions during apt install
    DEBIAN_FRONTEND="noninteractive"; \
    #allow start redis-server, mysql-server
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
    && apt-get install -y command-not-found bash-completion

#billing
RUN apt-get -y install nginx freeradius mysql-server \
    python3-pip python-requests \
    && systemctl enable freeradius

#clean
RUN \
    unset DEBIAN_FRONTEND \
    && unset RUNLEVEL \
    && echo 'debconf debconf/frontend select Dialog' | debconf-set-selections \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#billing
WORKDIR /var/www/billing
COPY . /var/www/billing
RUN pip3 install -r requirements.txt \
    && python3 manage.py collectstatic

#web
RUN pip3 install gunicorn \
    && cp docker/gunicorn.service /etc/systemd/system \
 #   && systemctl daemon-reload \
    && systemctl enable gunicorn \
    && cp docker/nginx-billing /etc/nginx/sites-available/billing \
    && ln -sr /etc/nginx/sites-available/billing /etc/nginx/sites-enabled/ \
    && rm -f /etc/nginx/sites-enabled/default

#freeradius
COPY 'docker/freeradius-billing_module_config' /etc/freeradius/3.0/mods-available/billing
COPY 'docker/freeradius-billing_site' /etc/freeradius/3.0/sites-available/billing
# echo -e
SHELL ["/bin/bash","-c"]
RUN cd /etc/freeradius/3.0/ \
    && ln -sr mods-available/billing mods-enabled/ \
    && ln -sr sites-available/billing sites-enabled/ \
    && mkdir billing \
    && cp mods-config/python/radiusd.py billing/ \ 
    && echo -e "client all{ \n\
    ipaddr = 0.0.0.0/0 \n\
    secret = testing123 \n\
    virtual_server = billing \n\
    } \n " >> /etc/freeradius/3.0/clients.conf

COPY 'docker/freeradius-billing_module_code' /etc/freeradius/3.0/billing/billing.py


VOLUME [ "/sys/fs/cgroup" ]

EXPOSE 8000 1812/udp 1813/udp

# ENTRYPOINT python3 manage.py runserver 0.0.0.0:8000
ENTRYPOINT ["/lib/systemd/systemd"]
