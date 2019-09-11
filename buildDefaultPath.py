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
                  ./autogen.sh && ./configure &&
                  make -j`grep -c ^processor /proc/cpuinfo` &&
                  mkdir -pv /tmp/build /tmp/deb && make install DESTDIR=/tmp/build &&
                  fpm -s dir -t deb -n cluster-libqb -v 0.17.2 -C /tmp/build -p /tmp/deb &&
                  cp /tmp/deb/* /exhaust/
                  '"""

corosyncCommand = """sh -c 'wget --no-check-certificate https://github.com/corosync/corosync/archive/v2.3.6.tar.gz &&
                     tar zxvf v2.3.6.tar.gz && cd /tmp/corosync-2.3.6 &&
                     dpkg -i /exhaust/cluster-libqb_0.17.2_amd64.deb &&
                     ./autogen.sh && ./configure &&
                     make -j`grep -c ^processor /proc/cpuinfo` &&
                     mkdir -pv /tmp/build /tmp/deb && make install DESTDIR=/tmp/build &&
                     fpm -s dir -t deb -n cluster-corosync -v 2.3.6 -C /tmp/build \
                     --before-install /exhaust/scripts/corosync/preinst \
                     --before-remove /exhaust/scripts/corosync/prerm \
                     --after-install /exhaust/scripts/corosync/postinst \
                     --after-remove /exhaust/scripts/corosync/postrm \
                     --deb-after-purge /exhaust/scripts/corosync/postrm \
                     -p /tmp/deb -d cluster-libqb -d libnss3 &&
                     cp /tmp/deb/* /exhaust/
                  '"""

cglueCommand = """sh -c 'wget --no-check-certificate https://github.com/ClusterLabs/cluster-glue/archive/glue-1.0.12.tar.gz &&
                     tar zxvf glue-1.0.12.tar.gz && cd /tmp/cluster-glue-glue-1.0.12 &&
                     dpkg -i /exhaust/*.deb && ./autogen.sh &&
                     ./configure --enable-fatal-warnings=no &&
                     make -j`grep -c ^processor /proc/cpuinfo` &&
                     mkdir -pv /tmp/build /tmp/deb && make install DESTDIR=/tmp/build &&
                     fpm -s dir -t deb -n cluster-cluster-glue -v 1.0.12 -C /tmp/build \
                     -p /tmp/deb -d cluster-libqb -d cluster-corosync &&
                     cp /tmp/deb/* /exhaust/
                  '"""

ragentsCommand = """sh -c 'wget --no-check-certificate https://github.com/ClusterLabs/resource-agents/archive/v3.9.7.tar.gz &&
                     tar zxvf v3.9.7.tar.gz && cd /tmp/resource-agents-3.9.7 &&
                     dpkg -i /exhaust/*.deb && ./autogen.sh &&
                     ./configure &&
                     make -j`grep -c ^processor /proc/cpuinfo` &&
                     mkdir -pv /tmp/build /tmp/deb && make install DESTDIR=/tmp/build &&
                     fpm -s dir -t deb -n cluster-resource-agents -v 3.9.7 -C /tmp/build \
                     -p /tmp/deb -d cluster-libqb -d cluster-corosync -d cluster-cluster-glue &&
                     cp /tmp/deb/* /exhaust/
                  '"""

pacemakerCommand = """sh -c 'wget --no-check-certificate https://github.com/ClusterLabs/pacemaker/archive/Pacemaker-1.1.16.tar.gz &&
                     tar zxvf Pacemaker-1.1.16.tar.gz && cd /tmp/pacemaker-Pacemaker-1.1.16 &&
                     dpkg -i /exhaust/*.deb && ./autogen.sh &&
                     ./configure &&
                     make -j`grep -c ^processor /proc/cpuinfo` &&
                     mkdir -pv /tmp/build /tmp/deb && make install DESTDIR=/tmp/build &&
                     fpm -s dir -t deb -n cluster-pacemaker -v 1.1.16 -C /tmp/build \
                     --after-install /exhaust/scripts/pacemaker/postinst \
                     -p /tmp/deb -d cluster-libqb -d cluster-corosync \
                     -d cluster-cluster-glue -d cluster-resource-agents &&
                     cp /tmp/deb/* /exhaust/
                  '"""

crmCommand = """sh -c 'wget --no-check-certificate https://github.com/ClusterLabs/crmsh/archive/2.1.9.tar.gz &&
                     tar zxvf 2.1.9.tar.gz && cd /tmp/crmsh-2.1.9 &&
                     dpkg -i /exhaust/*.deb && ./autogen.sh &&
                     ./configure &&
                     make -j`grep -c ^processor /proc/cpuinfo` &&
                     mkdir -pv /tmp/build /tmp/deb && make install DESTDIR=/tmp/build &&
                     fpm -s dir -t deb -n cluster-crmsh -v 2.1.9 -C /tmp/build \
                     -p /tmp/deb -d cluster-libqb -d cluster-corosync \
                     -d cluster-cluster-glue -d cluster-resource-agents \
                     -d cluster-pacemaker -d python-lxml &&
                     cp /tmp/deb/* /exhaust/
                  '"""

pythonCommand = """sh -c 'curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py &&
                     python get-pip.py && mkdir -pv wheels &&
                     pip wheel --wheel-dir wheels/ pip wheel parallel-ssh &&
                     pip install --no-index --find-links wheel pip wheel parallel_ssh &&
                  '"""

def main():
    buildImage('./prereq/', 'prereq')
    for command in libqbCommand, corosyncCommand, cglueCommand, ragentsCommand, pacemakerCommand, crmCommand:
        runContainer(command)
    #runContainer(corosyncCommand)

if __name__ == "__main__":
    client = docker.from_env()
    main()
    client.close()
