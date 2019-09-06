FROM astraglue

WORKDIR /tmp

RUN wget --no-check-certificate https://github.com/ClusterLabs/resource-agents/archive/v3.9.7.tar.gz
RUN tar zxvf v3.9.7.tar.gz

RUN dpkg -i /srv/*

WORKDIR /tmp/resource-agents-3.9.7

RUN ./autogen.sh \
    && ./configure \
    && make -j `grep -c ^processor /proc/cpuinfo` \
    && rm -rf /tmp/build \
    && mkdir -pv /tmp/build \
    && make install DESTDIR=/tmp/build

RUN fpm -s dir -t deb -n resource-agents -v 3.9.7 -C /tmp/build -p /srv
