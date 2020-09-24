Run:  
```bash
# MySQL fix:
sudo ln -s /etc/apparmor.d/usr.sbin.mysqld /etc/apparmor.d/disable/
sudo apparmor_parser -R /etc/apparmor.d/usr.sbin.mysqld

docker run --name=billing --privileged -d -p 1812:1812/udp -p 1813:1813/udp -p 80:80 -v/sys/fs/cgroup:/sys/fs/cgroup:ro pliuta/billing
```

Enter into:  
```bash 
docker exec -it billing /bin/bash
```
