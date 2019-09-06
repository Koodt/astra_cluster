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
    strace

RUN gem install --no-ri --no-rdoc ffi -v 1.10.0 \
    && gem install --no-ri --no-rdoc fpm
