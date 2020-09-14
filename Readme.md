docker run --rm --name=billing --privileged -d -p 1812:1812/udp -p 1813:1813/udp -p 80:80 -v/sys/fs/cgroup:/sys/fs/cgroup:ro pliuta/billing
