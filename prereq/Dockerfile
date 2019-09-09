FROM astra15

RUN apt-get update -y && apt-get install -y \
    wget \
    aptitude  \
    mc \
    build-essential \
    automake \
    autoconf \
    libtool \
    pkg-config \
    ruby \
    git \
    ruby-dev \
    rubygems \
    libnss3-dev \
    groff \
    strace \
    uuid-dev \
    libglib2.0-dev \
    libxml2-dev \
    libxslt1-dev \
    libbz2-dev \
    libncurses5-dev \
    python-lxml

RUN addgroup --system haclient \
    && adduser --system --no-create-home --ingroup haclient hacluster

RUN gem install --no-ri --no-rdoc ffi -v 1.10.0 \
    && gem install --no-ri --no-rdoc fpm
