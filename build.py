#!/usr/bin/python3

import docker
import os

def buildImage(dPath, dTag):
    client.images.build(path = dPath, tag = dTag, rm = True)

def runContainer(cCommand):
    client.containers.run(image = 'prereq', working_dir = '/tmp',
                          volumes = {os.getcwd() + '/exhaust': {'bind': '/exhaust', 'mode': 'rw'}},
                          command = cCommand, detach = False, remove = True)

libqbCommand = """sh -c 'wget --no-check-certificate https://github.com/ClusterLabs/libqb/releases/download/v0.17.2/libqb-0.17.2.tar.xz &&
                  tar Jxvf libqb-0.17.2.tar.xz && cd /tmp/libqb-0.17.2 &&
                  ./autogen.sh && ./configure --prefix=/opt/cluster &&
                  make -j`grep -c ^processor /proc/cpuinfo` &&
                  mkdir -pv /tmp/build /tmp/deb && make install DESTDIR=/tmp/build &&
                  fpm -s dir -t deb -n cluster-libqb -v 0.17.2 -C /tmp/build -p /tmp/deb &&
                  cp /tmp/deb/* /exhaust/
                  '"""

corosyncCommand = """sh -c 'wget --no-check-certificate https://github.com/corosync/corosync/releases/download/v2.4.5/corosync-2.4.5.tar.gz &&
                     tar zxvf corosync-2.4.5.tar.gz && cd /tmp/corosync-2.4.5 &&
                     dpkg -i /exhaust/* && ./autogen.sh &&
                     PATH="/opt/cluster/bin:$PATH" PKG_CONFIG_PATH="/opt/cluster/lib/pkgconfig" ./configure \
                     --prefix=/opt/cluster \
                     --bindir=/opt/cluster/bin \
                     --libdir=/opt/cluster/lib \
                     --sysconfdir=/etc \
                     --localstatedir=/var && make -j`grep -c ^processor /proc/cpuinfo` &&
                     mkdir -pv /tmp/build /tmp/deb && make install DESTDIR=/tmp/build &&
                     fpm -s dir -t deb -n cluster-corosync -v 2.4.5 -C /tmp/build -p /tmp/deb -d cluster-libqb &&
                     cp /tmp/deb/* /exhaust/
                  '"""

def main():
    buildImage('./prereq/', 'prereq')
    for command in libqbCommand, corosyncCommand:
        runContainer(command)

if __name__ == "__main__":
    client = docker.from_env()
    main()
    client.close()
