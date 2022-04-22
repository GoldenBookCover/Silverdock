
ARG SILVERDOCK_PHP_VERSION

FROM php:${SILVERDOCK_PHP_VERSION}-fpm-buster

# Set Environment Variables
ENV DEBIAN_FRONTEND noninteractive

ARG SILVERDOCK_PHP_VERSION

# Mandatory
RUN set -xe; \
    apt update -yqq \
    && apt-get install -y locales \
&& sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
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
    && php -m | grep -q '^zip$'
# Install php modules
RUN docker-php-ext-enable mysqli exif \
    && mv "${PHP_INI_DIR}/php.ini-production" "${PHP_INI_DIR}/php.ini"

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

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
        php -m | grep -oiE '^mongodb$'; \
    fi

# Install redis extension
ARG PHP_INSTALL_REDIS=false
RUN if [ ${PHP_INSTALL_REDIS} = true ]; then \
        pecl install -o -f redis \
        && rm -rf /tmp/pear \
        && docker-php-ext-enable redis; \
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

ARG PHP_INSTALL_PCNTL=false
RUN if [ ${PHP_INSTALL_PCNTL} = true ]; then \
    # Installs pcntl, helpful for running Horizon
    docker-php-ext-install pcntl \
;fi

ARG PHP_INSTALL_GRPC=false
RUN if [ ${PHP_INSTALL_GRPC} = true ]; then \
    # Install the grpc extension
    pecl install grpc && \
    docker-php-ext-enable grpc \
;fi

ARG PHP_INSTALL_PROTOBUF=false
RUN if [ ${PHP_INSTALL_PROTOBUF} = true ]; then \
    # Install the grpc extension
    pecl install protobuf-3.19.4 && \
    docker-php-ext-enable protobuf \
;fi

ARG PHP_INSTALL_SWOOLE=false
RUN set -eux; \
    if [ ${PHP_INSTALL_SWOOLE} = true ]; then \
      # Install Php Swoole Extension
      if [ $(php -r "echo PHP_MAJOR_VERSION;") = "5" ]; then \
        echo '' | pecl -q install swoole-2.0.10; \
      elif [ $(php -r "echo PHP_MAJOR_VERSION;") = "7" ] && [ $(php -r "echo PHP_MINOR_VERSION;") = "0" ]; then \
        echo '' | pecl -q install swoole-4.3.5; \
      elif [ $(php -r "echo PHP_MAJOR_VERSION;") = "7" ] && [ $(php -r "echo PHP_MINOR_VERSION;") = "1" ]; then \
        echo '' | pecl -q install swoole-4.5.11; \
      else \
        echo '' | pecl -q install swoole; \
      fi; \
      docker-php-ext-enable swoole; \
      php -m | grep -q '^swoole$'; \
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
ARG NODEJS_VERSION=16
RUN if [ ${INSTALL_NODEJS} = true ]; then \
        curl -sL https://deb.nodesource.com/setup_${NODEJS_VERSION}.x -o /tmp/setup.sh \
        && bash /tmp/setup.sh \
        && apt update \
        && apt -yqq install nodejs \
        && npm install yarn -g \
    ;fi

# Modify user and add ssh public key
ARG WORKSPACE_SSH_PUBKEY
RUN touch /usr/local/etc/php/conf.d/silver.ini \
    && groupadd -o -g ${PGID} silverdock \
    && useradd -o -u ${PUID} -g silverdock -s /bin/bash -m -c "SilverDock user" silverdock \
    && install -d -m 700 -o silverdock -g silverdock /home/silverdock/.ssh \
    && echo "$WORKSPACE_SSH_PUBKEY" > /home/silverdock/.ssh/authorized_keys \
    && chmod 600 /home/silverdock/.ssh/authorized_keys \
    && chown silverdock:silverdock /home/silverdock/.ssh/authorized_keys \
    && chmod 755 /usr/local/bin/entrypoint \
    && mkdir -p /var/www

WORKDIR /var/www
ENTRYPOINT [ "/usr/local/bin/entrypoint" ]

EXPOSE 22
