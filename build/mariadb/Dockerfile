ARG MARIADB_VERSION=latest
FROM mariadb:${MARIADB_VERSION}

#####################################
# Set Timezone
#####################################

ARG TZ=UTC
ARG MARIADB_REPLICA_STATE
ARG MARIADB_REPLICA_ID
ARG MARIADB_REPLICA_DATABASES
ENV TZ ${TZ}

COPY my.cnf /etc/mysql/conf.d/my.cnf
COPY export_database.sh /usr/local/bin/export_database

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && chown -R mysql:root /var/lib/mysql/ \
    && if [ ${MARIADB_REPLICA_STATE} = "master" ]; then \
        echo "ssl" >> /etc/mysql/conf.d/my.cnf; \
        echo "ssl-ca=/etc/mysql_ssl/ca-cert.pem" >> /etc/mysql/conf.d/my.cnf; \
        echo "ssl-cert=/etc/mysql_ssl/server-cert.pem" >> /etc/mysql/conf.d/my.cnf; \
        echo "ssl-key=/etc/mysql_ssl/server-key.pem" >> /etc/mysql/conf.d/my.cnf; \
        echo "server_id = ${MARIADB_REPLICA_ID}" >> /etc/mysql/conf.d/my.cnf; \
        echo "log_bin = /var/lib/mysql_data/bin_log/mysql-bin" >> /etc/mysql/conf.d/my.cnf; \
        echo "sync_binlog = 0" >> /etc/mysql/conf.d/my.cnf; \
        echo "expire_logs_days = 10" >> /etc/mysql/conf.d/my.cnf; \
        echo "binlog_cache_size = 128m" >> /etc/mysql/conf.d/my.cnf; \
        echo "max_binlog_cache_size = 512m" >> /etc/mysql/conf.d/my.cnf; \
        echo "max_binlog_size = 100m" >> /etc/mysql/conf.d/my.cnf; \
        echo "" >> /etc/mysql/conf.d/my.cnf; \
        echo "binlog-ignore-db = mysql" >> /etc/mysql/conf.d/my.cnf; \
        echo "binlog_ignore_db = information_schema" >> /etc/mysql/conf.d/my.cnf; \
        echo "binlog_ignore_db = performance_schema" >> /etc/mysql/conf.d/my.cnf; \
        echo "" >> /etc/mysql/conf.d/my.cnf; \
        for i in $(echo ${MARIADB_REPLICA_DATABASES} | tr "," " "); do \
            echo "binlog-do-db = $i" >> /etc/mysql/conf.d/my.cnf; \
        done; \
        install -d -m 755 -o mysql -g mysql /var/lib/mysql_data/bin_log; \
    elif [ ${MARIADB_REPLICA_STATE} = "slave" ]; then \
        echo "server_id = ${MARIADB_REPLICA_ID}" >> /etc/mysql/conf.d/my.cnf; \
        echo "relay_log = /var/lib/mysql_data/relay_log/static-relay-bin" >> /etc/mysql/conf.d/my.cnf; \
        echo "relay_log_index = /var/lib/mysql_data/relay_log/static-relay-bin.index" >> /etc/mysql/conf.d/my.cnf; \
        echo "relay_log_info_file = /var/lib/mysql_data/relay_log/relay-log.info" >> /etc/mysql/conf.d/my.cnf; \
        install -d -m 755 -o mysql -g mysql /var/lib/mysql_data/relay_log; \
    fi \
    && sed -i "/^databases/c databases='$(echo ${MARIADB_REPLICA_DATABASES} | tr ',' ' ')'" /usr/local/bin/export_database \
    && chmod 555 /usr/local/bin/export_database \
    && chmod 644 /etc/mysql/conf.d/my.cnf

# https://docs.docker.com/engine/reference/builder/#healthcheck
# https://github.com/MariaDB/mariadb-docker/blob/db55d2702dfc0102364a29ab00334b6a02085ef9/10.4/healthcheck.sh
HEALTHCHECK --interval=10s --timeout=9s --start-period=30s --retries=3 CMD [ "/usr/local/bin/healthcheck.sh", "--connect" ]

CMD ["mysqld"]

EXPOSE 3306
