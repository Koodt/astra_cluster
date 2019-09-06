FROM astralibqb

WORKDIR /tmp

RUN wget --no-check-certificate https://github.com/corosync/corosync/releases/download/v2.4.5/corosync-2.4.5.tar.gz
RUN tar zxvf corosync-2.4.5.tar.gz

RUN dpkg -i /srv/*

WORKDIR /tmp/corosync-2.4.5

RUN ./autogen.sh \
    && ./configure \
    && make -j `grep -c ^processor /proc/cpuinfo` \
    && rm -rf /tmp/build \
    && mkdir -pv /tmp/build \
    && make install DESTDIR=/tmp/build

RUN fpm -s dir -t deb -n corosync -v 2.4.5 -C /tmp/build -p /srv
