
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

# Modify user
# "#SilverDock cron job\n* * * * * www-data /usr/local/bin/php /usr/share/nginx/${PROJECT_NAME}/artisan schedule:run &> /dev/null"
RUN chmod 755 /usr/local/bin/entrypoint \
    && groupmod -o -g ${PGID} www-data \
    && usermod -o -u ${PUID} -g www-data www-data \
    && chown www-data:www-data /var/www \
    && chmod 755 /usr/local/bin/entrypoint \
    && echo "#SilverDock cron job\n* * * * * www-data /usr/local/bin/php /usr/share/nginx/${PROJECT_NAME}/artisan schedule:run &> /tmp/test.log" | tee -a /etc/crontab \
    && mkdir -p /usr/share/nginx/${PROJECT_NAME}
# USER www-data
WORKDIR /usr/share/nginx/${PROJECT_NAME}
CMD [ "/usr/local/bin/entrypoint" ]

EXPOSE 9000
