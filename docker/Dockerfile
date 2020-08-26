FROM ubuntu:20.04

ENV container=docker LC_ALL=C

RUN sed -i 's/# deb/deb/g' /etc/apt/sources.list \
    #allow work with services
    && rm -f /usr/sbin/policy-rc.d \
    && dpkg-divert --remove /sbin/initctl \
    && rm -f /sbin/initctl \
    #do not ask questions during apt install
    && export DEBIAN_FRONTEND="noninteractive" \
    #allow start redis-server (mysql-server)
    && export RUNLEVEL=5 \
    && apt-get update \
    && apt-get install -y apt-utils \
    && apt-get install -y dialog \
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
    && apt-get install -y command-not-found bash-completion \
    #billing
    && apt -y install nginx freeradius mysql-server \
    #clean
    && unset DEBIAN_FRONTEND \
    && unset RUNLEVEL \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

VOLUME [ "/sys/fs/cgroup" ]

EXPOSE 80 8080 443 1812/udp 1813/udp

ENTRYPOINT ["/lib/systemd/systemd"]
