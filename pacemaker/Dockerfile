FROM astraagents

WORKDIR /tmp

RUN wget --no-check-certificate https://github.com/ClusterLabs/pacemaker/archive/Pacemaker-1.1.21.tar.gz
RUN tar zxvf Pacemaker-1.1.21.tar.gz

RUN addgroup --system haclient \
    && adduser --system --no-create-home --ingroup haclient hacluster

RUN dpkg -i /srv/*

WORKDIR /tmp/pacemaker-Pacemaker-1.1.21

RUN ./autogen.sh \
    && ./configure \
    && make -j `grep -c ^processor /proc/cpuinfo` \
    && rm -rf /tmp/build \
    && mkdir -pv /tmp/build \
    && make install DESTDIR=/tmp/build

RUN fpm -s dir -t deb -n pacemaker -v 1.1.21 -C /tmp/build -p /srv
