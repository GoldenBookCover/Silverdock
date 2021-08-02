
ARG SILVERDOCK_PHP_VERSION

FROM php:${SILVERDOCK_PHP_VERSION}-fpm-buster

LABEL maintainer="Monstre Charmant <https://github.com/MonstreCharmant>"

# Set Environment Variables
ENV DEBIAN_FRONTEND noninteractive

ARG SILVERDOCK_PHP_VERSION

# Mandatory
RUN set -xe; \
    apt update -yqq \
    && pecl channel-update pecl.php.net \
    && apt install -yqq \
        apt-utils \
        ca-certificates \
        cron \
        curl \
        git \
        gnupg2 \
        libxml2-dev \
        libzip-dev \
        libmcrypt-dev \
        lsb-release \
        unzip \
        vim \
        zip \
        sudo \
        man-db \
        bash-completion \
    && if [ ${SILVERDOCK_PHP_VERSION} = "7.3" ] || [ ${SILVERDOCK_PHP_VERSION} = "7.4" ] || [ $(php -r "echo PHP_MAJOR_VERSION;") = "8" ]; then \
        docker-php-ext-configure zip; \
    else \
        docker-php-ext-configure zip --with-libzip; \
    fi \
    && docker-php-ext-install zip pdo_mysql mysqli exif bcmath \
    && php -m | grep -q 'zip' \
    && pecl install mcrypt
# Install php modules
RUN docker-php-ext-enable mysqli exif mcrypt \
    && mv "${PHP_INI_DIR}/php.ini-production" "${PHP_INI_DIR}/php.ini"

# Optional
# Install gi
ARG PHP_INSTALL_GD=false
RUN if [ ${PHP_INSTALL_GD} = true ]; then \
        apt install -yqq \
            libfreetype6-dev \
            libjpeg62-turbo-dev \
            libpng-dev \
            libwebp-dev \
        && if [ ${SILVERDOCK_PHP_VERSION} = "7.3" ]; then \
            docker-php-ext-configure gd \
                --with-freetype-dir=/usr/include/ \
                --with-jpeg-dir=/usr/include/ \
                --with-webp-dir=/usr/include/; \
        else \
            docker-php-ext-configure gd \
                --with-freetype \
                --with-jpeg \
                --with-webp; \
        fi \
        && docker-php-ext-install gd; \
    fi

# Install gmp
ARG PHP_INSTALL_GMP=false
RUN if [ ${PHP_INSTALL_GMP} = true ]; then \
        apt install -yqq libgmp-dev \
        && if [ $(php -r "echo PHP_MAJOR_VERSION;") = "5" ]; then \
            ln -s /usr/include/x86_64-linux-gnu/gmp.h /usr/include/gmp.h; \
        fi \
        && docker-php-ext-install gmp; \
    fi

# Install mongo extension
ARG PHP_INSTALL_MONGO=false
RUN if [ ${PHP_INSTALL_MONGO} = true ]; then \
        apt install -yqq libcurl4-openssl-dev libssl-dev \
        && pecl install mongodb \
        && docker-php-ext-enable mongodb; \
    fi

# Install redis extension
ARG PHP_INSTALL_REDIS=false
RUN if [ ${PHP_INSTALL_REDIS} = true ]; then \
        mkdir -p /usr/src/php/ext/redis \
        && curl -L https://github.com/phpredis/phpredis/archive/5.3.2.tar.gz \
            | tar -zxv -C /usr/src/php/ext/redis --strip 1 \
        && echo "redis" | tee -a /usr/src/php-available-exts \
        && docker-php-ext-install redis; \
    fi

# Install opencc extension
ARG PHP_INSTALL_OPENCC=false
RUN if [ ${PHP_INSTALL_OPENCC} = true ]; then \
        apt install -y -q libopencc-dev \
        && mkdir -p /usr/src/php/ext/opencc4php \
        && git clone https://github.com/nauxliu/opencc4php.git /usr/src/php/ext/opencc4php \
        && echo "opencc4php" | tee -a /usr/src/php-available-exts \
        && docker-php-ext-install opencc4php; \
    fi

# Install composer
RUN curl -sS https://getcomposer.org/installer | php \
    && install -m 755 composer.phar /usr/bin/composer \
    && rm -f composer.phar

ARG PROJECT_NAME=html
ARG PUID=1000
ENV PUID ${PUID}
ARG PGID=1000
ENV PGID ${PGID}

# Import entrypoint script to control startup
COPY entrypoint.sh /usr/local/bin/entrypoint

# Different from php-fpm from here
RUN apt install -yqq \
        openssh-server \
        mariadb-client \
        dos2unix

# Add sshd config
COPY sshd_config /etc/ssh/sshd_config

RUN if [ ${PHP_INSTALL_REDIS} = true ]; then \
        apt install -yqq redis; \
    fi

ARG SIRVERDOCK_MONGO_VERSION="4.4"
RUN if [ ${PHP_INSTALL_MONGO} = true ]; then \
        apt -y install gnupg \
        && curl -so - https://www.mongodb.org/static/pgp/server-${SIRVERDOCK_MONGO_VERSION}.asc | apt-key add - \
        && echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/${SIRVERDOCK_MONGO_VERSION} main" | tee /etc/apt/sources.list.d/mongodb-org-${SIRVERDOCK_MONGO_VERSION}.list \
        && apt update \
        && apt -yqq install mongodb-org-shell; \
    fi

ARG PHP_INSTALL_WPCLI=false
RUN if [ ${PHP_INSTALL_WPCLI} = true ]; then \
        curl -sL https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -o /usr/local/bin/wp \
        && chmod 755 /usr/local/bin/wp; \
    fi

ARG INSTALL_NODEJS=false
ARG NODEJS_VERSION=14
RUN if [ ${INSTALL_NODEJS} = true ]; then \
        curl -sL https://deb.nodesource.com/setup_${NODEJS_VERSION}.x -o /tmp/setup.sh \
        && bash /tmp/setup.sh \
        && apt update \
        && apt -yqq install nodejs \
        && npm install yarn -g \
    ;fi

# Modify user and add ssh public key
RUN groupadd -o -g ${PGID} silverdock \
    && useradd -o -u ${PUID} -g silverdock -s /bin/bash -m -c "SilverDock user" silverdock \
    && install -d -m 700 -o silverdock -g silverdock /home/silverdock/.ssh

# USER silverdock
COPY silverdock.pem.pub /home/silverdock/.ssh/authorized_keys

RUN chmod 600 /home/silverdock/.ssh/authorized_keys \
    && chown silverdock:silverdock /home/silverdock/.ssh/authorized_keys \
    && chmod 755 /usr/local/bin/entrypoint \
    && mkdir -p /usr/share/nginx/${PROJECT_NAME}

WORKDIR /usr/share/nginx/${PROJECT_NAME}
CMD [ "/usr/local/bin/entrypoint" ]
EXPOSE 22
