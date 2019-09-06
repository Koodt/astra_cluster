FROM astraprereq

WORKDIR /tmp

RUN wget --no-check-certificate https://github.com/ClusterLabs/libqb/releases/download/v0.17.2/libqb-0.17.2.tar.xz
RUN tar Jxvf libqb-0.17.2.tar.xz

WORKDIR /tmp/libqb-0.17.2

RUN ./autogen.sh \
    && ./configure \
    && make -j `grep -c ^processor /proc/cpuinfo` \
    && mkdir -pv /tmp/build \
    && make install DESTDIR=/tmp/build

RUN fpm -s dir -t deb -n libqb -v 0.17.2 -C /tmp/build -p /srv
