This project is a course work (https://rivne.itstep.org/programmer)
The project implements simple billing system for internet providers. 
Only Mikrotik routers are supported to be Network Access Servers (NAS, router)
System allows manipulate of: customers, finance transactions, internet tariffs, routers

Used technologies: 
Docker, Dockerhub, Ubuntu, MySQL, Nginx, Gunicorn, Freeradius, Django, Django-admin

### Run container:  
```bash
# MySQL fix for host system:
sudo ln -s /etc/apparmor.d/usr.sbin.mysqld /etc/apparmor.d/disable/
sudo apparmor_parser -R /etc/apparmor.d/usr.sbin.mysqld

docker run --name=billing --privileged -d -p 1812:1812/udp -p 1813:1813/udp -p 80:80 -v/sys/fs/cgroup:/sys/fs/cgroup:ro pliuta/billing
```

### Enter into container:  
```bash 
docker exec -it billing /bin/bash
```

### Links:
Docker-hub: https://hub.docker.com/r/pliuta/billing  
Video (course work defence, up to 45 min): https://youtu.be/E7PxUpw-XJ4  
