ARG SILVERDOCK_PHP_VERSION
FROM php:${SILVERDOCK_PHP_VERSION}-alpine

ARG SILVERDOCK_PHP_VERSION

# If you're in China, or you need to change sources, will be set CHANGE_SOURCE to true in .env.
ARG CHANGE_SOURCE=false
RUN if [ ${CHANGE_SOURCE} = true ]; then \
        sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/' /etc/apk/repositories; \
    fi

# Initial dependencies
RUN apk --update add \
        autoconf \
        build-base \
        curl \
        cyrus-sasl-dev \
        git \
        libgsasl-dev \
        libmcrypt-dev \
        libressl \
        libressl-dev \
        libxml2-dev \
        linux-headers \
        oniguruma-dev \
        pcre-dev \
        wget \
        zlib-dev \
        supervisor; \
    mkdir -p /var/log/supervisord

# Basic php modules
RUN pecl channel-update pecl.php.net; \
    docker-php-ext-install \
        exif \
        mbstring \
        mysqli \
        pdo \
        pdo_mysql \
        xml \
    ; \
    if [ $(php -r "echo PHP_MAJOR_VERSION;") = "8" ] && [ $(php -r "echo PHP_MINOR_VERSION;") = "1" ]; then \
        php -m | grep -q 'tokenizer'; \
    else \
        docker-php-ext-install tokenizer; \
    fi

#Install GD package
ARG INSTALL_GD=false
RUN if [ ${INSTALL_GD} = true ]; then \
        apk add --update --no-cache freetype-dev libjpeg-turbo-dev jpeg-dev libpng-dev; \
        if [ $(php -r "echo PHP_MAJOR_VERSION;") = "7" ] && [ $(php -r "echo PHP_MINOR_VERSION;") = "4" ]; then \
            docker-php-ext-configure gd --with-freetype --with-jpeg --with-png; \
        else \
            docker-php-ext-configure gd --with-freetype-dir=/usr/lib/ --with-jpeg-dir=/usr/lib/ --with-png-dir=/usr/lib/; \
        fi; \
        docker-php-ext-install gd; \
        php -m | grep -oiE '^gd$'; \
    fi

#Install GMP package
ARG INSTALL_GMP=false
RUN if [ ${INSTALL_GMP} = true ]; then \
        apk add --update --no-cache gmp gmp-dev && \
        docker-php-ext-install gmp; \
        php -m | grep -oiE '^gmp$'; \
    fi

#Install BCMath package
ARG INSTALL_BCMATH=false
RUN if [ ${INSTALL_BCMATH} = true ]; then \
        docker-php-ext-install bcmath; \
        php -m | grep -oiE '^bcmath$'; \
    fi

# Install MongoDB drivers
ARG INSTALL_MONGO=false
RUN if [ ${INSTALL_MONGO} = true ]; then \
        if [ $(php -r "echo PHP_MAJOR_VERSION;") = "7" ] && { [ $(php -r "echo PHP_MINOR_VERSION;") = "0" ] || [ $(php -r "echo PHP_MINOR_VERSION;") = "1" ] ;}; then \
            pecl install mongodb-1.9.2; \
        else \
            pecl install mongodb; \
        fi; \
        docker-php-ext-enable mongodb; \
        php -m | grep -oiE '^mongodb$'; \
    fi

# Install ZipArchive
ARG INSTALL_ZIP_ARCHIVE=false
RUN set -eux; \
    if [ ${INSTALL_ZIP_ARCHIVE} = true ]; then \
        apk --update add libzip-dev && \
        if [ ${SILVERDOCK_PHP_VERSION} = "7.3" ] || [ ${SILVERDOCK_PHP_VERSION} = "7.4" ] || [ $(php -r "echo PHP_MAJOR_VERSION;") = "8" ]; then \
            docker-php-ext-configure zip; \
        else \
            docker-php-ext-configure zip --with-libzip; \
        fi && \
        docker-php-ext-install zip; \
        php -m | grep -oiE '^zip$'; \
    fi

# Install MySQL Client
ARG INSTALL_MYSQL_CLIENT=false
RUN if [ ${INSTALL_MYSQL_CLIENT} = true ]; then \
        apk --update add mysql-client; \
    fi

# Install FFMPEG
ARG INSTALL_FFMPEG=false
RUN if [ ${INSTALL_FFMPEG} = true ]; then \
        apk --update add ffmpeg \
    ;fi

# Install Redis package
ARG INSTALL_REDIS=false
RUN if [ ${INSTALL_REDIS} = true ]; then \
        printf "\n" | pecl install -o -f redis; \
        rm -rf /tmp/pear; \
        docker-php-ext-enable redis; \
        php -m | grep -oiE '^redis$'; \
    fi

# Install pcntl
ARG INSTALL_PCNTL=false
RUN if [ ${INSTALL_PCNTL} = true ]; then \
    # Installs pcntl, helpful for running Horizon
    docker-php-ext-install pcntl \
;fi

# Install grpc
ARG INSTALL_GRPC=false
RUN if [ ${INSTALL_GRPC} = true ]; then \
    # Install the grpc extension
    pecl install grpc && \
    docker-php-ext-enable grpc \
;fi

# Install protobuf
ARG INSTALL_PROTOBUF=false
RUN if [ ${INSTALL_PROTOBUF} = true ]; then \
        pecl install protobuf-3.19.4 && \
        docker-php-ext-enable protobuf; \
        php -m | grep -oiE '^protobuf$'; \
    fi

# Install Swoole
ARG INSTALL_SWOOLE=false
RUN set -eux; \
    if [ ${INSTALL_SWOOLE} = true ]; then \
        if [ $(php -r "echo PHP_VERSION_ID - PHP_RELEASE_VERSION;") = "70000" ]; then \
            pecl install swoole-4.3.5; \
        elif [ $(php -r "echo PHP_VERSION_ID - PHP_RELEASE_VERSION;") = "70100" ]; then \
            pecl install swoole-4.5.11; \
        else \
            pecl install swoole; \
        fi; \
        docker-php-ext-enable swoole; \
        php -m | grep -oiE '^swoole$'; \
    fi

# Install opencc extension
# TODO: Adapt to alpine
ARG INSTALL_OPENCC=false
# RUN if [ ${INSTALL_OPENCC} = true ]; then \
#         apt install -y -q libopencc-dev \
#         && mkdir -p /usr/src/php/ext/opencc4php \
#         && git clone https://github.com/nauxliu/opencc4php.git /usr/src/php/ext/opencc4php \
#         && echo "opencc4php" | tee -a /usr/src/php-available-exts \
#         && docker-php-ext-install opencc4php; \
#     fi

COPY supervisord.conf /etc/supervisord.conf

ENTRYPOINT ["/usr/bin/supervisord", "-n", "-c",  "/etc/supervisord.conf"]

# Optional Software's Installation

# Check PHP version
RUN php -v | grep -q "^PHP ${SILVERDOCK_PHP_VERSION}."

ARG PUID=1000
ENV PUID ${PUID}
ARG PGID=1000
ENV PGID ${PGID}

RUN apk add shadow && \
    groupadd -o -g ${PGID} silverdock && \
    useradd -g silverdock -o -u ${PUID} silverdock

# Clean up
RUN rm /var/cache/apk/* \
    && mkdir -p /var/www

WORKDIR /etc/supervisor/conf.d/
