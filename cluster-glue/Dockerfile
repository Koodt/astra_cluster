FROM astracoro

WORKDIR /tmp

RUN apt-get update -y && apt-get install -y \
    uuid-dev \
    libglib2.0-dev \
    libxml2-dev \
    libxslt1-dev \
    libbz2-dev \
    libncurses5-dev

RUN wget --no-check-certificate https://github.com/ClusterLabs/cluster-glue/archive/glue-1.0.12.tar.gz
RUN tar zxvf glue-1.0.12.tar.gz

RUN dpkg -i /srv/*

WORKDIR /tmp/cluster-glue-glue-1.0.12

RUN ./autogen.sh \
    && ./configure --enable-fatal-warnings=no \
    && make -j `grep -c ^processor /proc/cpuinfo` \
    && rm -rf /tmp/build \
    && mkdir -pv /tmp/build \
    && make install DESTDIR=/tmp/build

RUN fpm -s dir -t deb -n cluster-glue -v 1.0.12 -C /tmp/build -p /srv
