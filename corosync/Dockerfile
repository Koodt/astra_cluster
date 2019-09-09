FROM compose_prereq

WORKDIR /tmp

RUN wget --no-check-certificate https://github.com/corosync/corosync/releases/download/v2.4.5/corosync-2.4.5.tar.gz
RUN tar zxvf corosync-2.4.5.tar.gz

RUN dpkg -i /exhaust/*

WORKDIR /tmp/corosync-2.4.5

RUN ./autogen.sh \
    && PATH="/opt/cluster/bin:$PATH" PKG_CONFIG_PATH="/opt/cluster/lib/pkgconfig" \
    ./configure \
    --prefix=/opt/cluster \
    --bindir=/opt/cluster/bin \
    --libdir=/opt/cluster/lib \
    --sysconfdir=/etc \
    --localstatedir=/var \
    && make -j`grep -c ^processor /proc/cpuinfo` \
    && rm -rf /tmp/build \
    && mkdir -pv /tmp/build \
    && make install DESTDIR=/tmp/build

RUN fpm -s dir -t deb -n cluster-corosync -v 2.4.5 -C /tmp/build -p /srv -d cluster-libqb
