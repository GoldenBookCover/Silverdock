
ARG SILVERDOCK_PHP_VERSION
ARG OS_PREFER=bookworm

FROM php:${SILVERDOCK_PHP_VERSION}-fpm-${OS_PREFER}

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
        lsb-release \
        unzip \
        vim \
        zip \
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

# Optional
# Install gd
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
ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
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

ARG PHP_INSTALL_FFMPEG=false
RUN set -eux; \
    if [ ${PHP_INSTALL_FFMPEG} = true ]; then \
      # Install ffmpeg & ffprobe binaries
      apt update; \
      apt install -yqq ffmpeg; \
    fi

ARG PHP_INSTALL_INTL=false
RUN set -eux; \
    if [ ${PHP_INSTALL_INTL} = true ]; then \
      # Install php intl Extension
      docker-php-ext-install intl; \
      php -m | grep -q '^intl$'; \
    fi

ARG PUID=1000
ENV PUID=${PUID}
ARG PGID=1000
ENV PGID=${PGID}
ARG ENABLE_CRONJOB=false
ENV ENABLE_CRONJOB=${ENABLE_CRONJOB}


# Import entrypoint script to control startup
COPY entrypoint.sh /usr/local/bin/entrypoint

# Modify user
RUN apt update \
    && apt install gosu -yqq \
    && chmod 755 /usr/local/bin/entrypoint \
    && touch /usr/local/etc/php/conf.d/silver.ini \
    && groupmod -o -g ${PGID} www-data \
    && usermod -o -u ${PUID} -g www-data www-data \
    && echo "#SilverDock cron job\n* * * * * www-data /usr/local/bin/php /var/www/artisan schedule:run > /dev/null 2>&1\n" >> /etc/crontab \
    && mkdir -p /var/www

WORKDIR /var/www
ENTRYPOINT [ "/usr/local/bin/entrypoint" ]
CMD [ "php-fpm" ]

EXPOSE 9000
EXPOSE 8000
