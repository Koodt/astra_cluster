FROM astrapacemaker

RUN apt-get update -y && apt-get install -y \
    python-lxml

WORKDIR /tmp

RUN wget --no-check-certificate https://github.com/ClusterLabs/crmsh/archive/2.1.9.tar.gz
RUN tar zxvf 2.1.9.tar.gz

RUN dpkg -i /srv/*

WORKDIR /tmp/crmsh-2.1.9

RUN ./autogen.sh \
    && ./configure \
    && make -j `grep -c ^processor /proc/cpuinfo` \
    && rm -rf /tmp/build \
    && mkdir -pv /tmp/build \
    && make install DESTDIR=/tmp/build

RUN fpm -s dir -t deb -n crmsh -v 2.1.9 -C /tmp/build -p /srv
