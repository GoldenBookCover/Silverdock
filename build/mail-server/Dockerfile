
ARG SILVERDOCK_PYTHON_VERSION
FROM debian:bullseye

ARG PUBLIC_IP
ARG MAIL_DOMAIN
ARG MAIL_TOP_DOMAIN
ARG FQDN
ARG DB_DATABASE
ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_HOST
# Disable prompt when installing packages
ENV DEBIAN_FRONTEND "noninteractive"

COPY . /data

# Essentials
RUN apt -y update \
    && apt -y -q install \
        rsyslog \
        procps \
        net-tools \
        ca-certificates \
        openssl \
        curl \
        mariadb-client \
        bsd-mailx \
        vim \
    && cp /data/entrypoint.sh /usr/local/bin/entrypoint \
    && chmod 755 /usr/local/bin/entrypoint

# Install postfix
RUN apt -y -q install postfix postfix-mysql \
    && if [ "x${FQDN}" = "x" ]; then \
        echo "${PUBLIC_IP} ${MAIL_DOMAIN}" >> /etc/hosts; \
    else \
        echo "${PUBLIC_IP} ${FQDN} $(echo ${FQDN} | cut -d. -f1)" >> /etc/hosts; \
    fi \
    && groupadd -g 5000 vmail \
    && useradd -g vmail -u 5000 vmail -d /var/mail/ \
    && postconf -e "alias_database = hash:/etc/aliases" \
    && postconf -e "alias_maps = hash:/etc/aliases" \
    && postconf -e "append_dot_mydomain = no" \
    && postconf -e "biff = no" \
    && postconf -e "compatibility_level = 2" \
    && postconf -e "inet_interfaces = all" \
    && postconf -e "inet_protocols = all" \
    && postconf -e "mailbox_size_limit = 0" \
    && postconf -e "milter_default_action = accept" \
    && postconf -e "milter_protocol = 6" \
    && postconf -e "mydestination = localhost, localhost.\$mydomain" \
    && postconf -e "mydomain = ${MAIL_TOP_DOMAIN}" \
    && postconf -e "myhostname = ${MAIL_DOMAIN}" \
    && postconf -e "mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128 172.16.0.0/12" \
    && postconf -e "myorigin = \$mydomain" \
    && postconf -e "non_smtpd_milters = inet:127.0.0.1:8891" \
    && postconf -e "readme_directory = no" \
    && postconf -e "recipient_delimiter = +" \
    && postconf -e "relayhost =" \
    && postconf -e "smtp_tls_CApath = /etc/ssl/certs" \
    && postconf -e "smtp_tls_security_level = may" \
    && postconf -e "smtpd_banner = \$myhostname ESMTP \$mail_name (Debian/GNU)" \
    && postconf -e "smtpd_milters = inet:127.0.0.1:8891" \
    && postconf -e "smtpd_client_restrictions = permit_sasl_authenticated" \
    && postconf -e "smtpd_recipient_restrictions = permit_sasl_authenticated check_sender_access hash:/etc/postfix/sender_access check_recipient_access hash:/etc/postfix/filtered_domains permit_mynetworks reject_unauth_destination" \
    && postconf -e "smtpd_relay_restrictions = permit_mynetworks permit_sasl_authenticated defer_unauth_destination" \
    && postconf -e "smtpd_sasl_security_options = noanonymous, noplaintext" \
    && postconf -e "smtpd_sasl_tls_security_options = noanonymous" \
    && postconf -e "smtpd_sender_login_maps = mysql:/etc/postfix/mysql-virtual-mailbox-maps.cf" \
    && postconf -e "smtpd_tls_auth_only = yes" \
    && postconf -e "smtpd_tls_cert_file = /etc/letsencrypt/live/${MAIL_DOMAIN}/fullchain.pem" \
    && postconf -e "smtpd_tls_key_file = /etc/letsencrypt/live/${MAIL_DOMAIN}/privkey.pem" \
    && postconf -e "smtpd_tls_security_level = may" \
    && postconf -e "smtpd_use_tls = yes" \
    && postconf -e "virtual_alias_maps = mysql:/etc/postfix/mysql-virtual-alias-maps.cf," \
    && postconf -e "virtual_mailbox_domains = mysql:/etc/postfix/mysql-virtual-mailbox-domains.cf" \
    && postconf -e "virtual_mailbox_maps = mysql:/etc/postfix/mysql-virtual-mailbox-maps.cf" \
    && postconf -e "virtual_transport = lmtp:unix:private/dovecot-lmtp" \
    && postconf -e "virtual_uid_maps = static:5000" \
    && postconf -e "virtual_gid_maps = static:5000" \
    && postconf -e "virtual_mailbox_base = /var/mail/vhosts" \
    && echo "user = ${DB_USERNAME}\npassword = ${DB_PASSWORD}\nhosts = ${DB_HOST}\ndbname = ${DB_DATABASE}\nquery = SELECT destination FROM forwardings WHERE source='%s'" >> /etc/postfix/mysql-virtual-alias-maps.cf \
    && echo "user = ${DB_USERNAME}\npassword = ${DB_PASSWORD}\nhosts = ${DB_HOST}\ndbname = ${DB_DATABASE}\nquery = SELECT email FROM users WHERE email='%s'" >> /etc/postfix/mysql-virtual-email2email.cf \
    && echo "user = ${DB_USERNAME}\npassword = ${DB_PASSWORD}\nhosts = ${DB_HOST}\ndbname = ${DB_DATABASE}\nquery = SELECT domain AS virtual FROM domains WHERE domain='%s'" >> /etc/postfix/mysql-virtual-mailbox-domains.cf \
    && echo "user = ${DB_USERNAME}\npassword = ${DB_PASSWORD}\nhosts = ${DB_HOST}\ndbname = ${DB_DATABASE}\nquery = SELECT CONCAT(SUBSTRING_INDEX(email,'@',-1),'/',SUBSTRING_INDEX(email,'@',1),'/') FROM users WHERE email='%s'" >> /etc/postfix/mysql-virtual-mailbox-maps.cf \
    && cp /data/_etc/postfix/master.cf /etc/postfix/master.cf \
    && touch /etc/postfix/sender_access /etc/postfix/filtered_domains \
    && postmap hash:/etc/postfix/sender_access \
    && postmap hash:/etc/postfix/filtered_domains \
    && cp /data/deny_email.sh /usr/local/bin/deny_email \
    && chmod 755 /usr/local/bin/deny_email

# Install spamassassin
ARG ENABLE_SPAMASSASSIN
RUN if [ ${ENABLE_SPAMASSASSIN} = true ]; then \
        apt -y -q install \
            spamassassin \
            spamc \
            postfix-pcre \
    ; fi \
    && cp /data/_etc/spamassassin/*.cf /etc/mail/spamassassin/

# Install opendkim
ARG ENABLE_OPENDKIM
RUN if [ ${ENABLE_OPENDKIM} = true ]; then \
        apt -y -q install \
            opendkim \
            opendkim-tools \
    ; fi \
    && cp /data/_etc/opendkim.conf /etc/opendkim.conf \
    && install -d -m 755 -o opendkim -g opendkim /etc/opendkim \
    && install -d -m 700 -o opendkim -g opendkim /etc/opendkim/keys \
    && echo "default._domainkey.${MAIL_TOP_DOMAIN} ${MAIL_TOP_DOMAIN}:default:/etc/opendkim/keys/${MAIL_TOP_DOMAIN}/default.private" > /etc/opendkim/KeyTable \
    && echo "*@${MAIL_TOP_DOMAIN} default._domainkey.${MAIL_TOP_DOMAIN}" > /etc/opendkim/SigningTable \
    && echo "127.0.0.1\n::1\n*.${MAIL_TOP_DOMAIN}" > /etc/opendkim/TrustedHosts \
    && install -d -m 755 -o opendkim -g opendkim /etc/opendkim/keys/${MAIL_TOP_DOMAIN}

# Generate new opendkim keys
ARG GENERATE_OPENDKIM_KEY
RUN if [ ${GENERATE_OPENDKIM_KEY} = true ]; then \
        cd /etc/opendkim/keys/${MAIL_TOP_DOMAIN} \
        && opendkim-genkey -s default -d ${MAIL_TOP_DOMAIN} \
        && chown opendkim:opendkim default.private default.txt \
    ; fi

# Install dovecot
RUN apt -y -q install \
        dovecot-core \
        dovecot-mysql \
        dovecot-imapd \
        dovecot-pop3d \
        dovecot-lmtpd \
    && cp /data/_etc/dovecot/conf.d/10-auth.conf /etc/dovecot/conf.d/ \
    && cp /data/_etc/dovecot/conf.d/10-mail.conf /etc/dovecot/conf.d/ \
    && cp /data/_etc/dovecot/conf.d/10-master.conf /etc/dovecot/conf.d/ \
    && cp /data/_etc/dovecot/conf.d/auth-sql.conf.ext /etc/dovecot/conf.d/ \
    && cp /data/_etc/dovecot/conf.d/15-mailboxes.conf /etc/dovecot/conf.d/ \
    && sed -i "/^ssl =/c ssl = required" /etc/dovecot/conf.d/10-ssl.conf \
    && sed -i "/^ssl_cert =/c ssl_cert = </etc/letsencrypt/live/${MAIL_DOMAIN}/fullchain.pem" /etc/dovecot/conf.d/10-ssl.conf \
    && sed -i "/^ssl_key =/c ssl_key = </etc/letsencrypt/live/${MAIL_DOMAIN}/privkey.pem" /etc/dovecot/conf.d/10-ssl.conf \
    && cp /data/_etc/dovecot/dovecot-sql.conf.ext /etc/dovecot/ \
    && sed -i "/^connect/c connect = host=${DB_HOST} dbname=${DB_DATABASE} user=${DB_USERNAME} password=${DB_PASSWORD}" /etc/dovecot/dovecot-sql.conf.ext \
    && install -d -m 755 -o vmail -g vmail /var/mail/vhosts/${MAIL_TOP_DOMAIN} \
    && chown -R vmail:dovecot /etc/dovecot

# Install dovecot sieve plugin
ARG ENABLE_SIEVE
RUN if [ ${ENABLE_SIEVE} = true ]; then \
        apt -y -q install \
            dovecot-sieve \
    ; fi \
    && cp /data/_etc/dovecot/conf.d/90-sieve.conf /etc/dovecot/conf.d/ \
    && sed -i '/mail_plugins =/a \ \ mail_plugins = \$mail_plugins sieve' /etc/dovecot/conf.d/15-lda.conf \
    && sed -i '/sieve_before =/a \ \ sieve_before = /var/mail/SpamToJunk.sieve' /etc/dovecot/conf.d/90-sieve.conf \
    && cp /data/_etc/dovecot/SpamToJunk.sieve /var/mail/ \
    && sievec /var/mail/SpamToJunk.sieve

RUN echo "Opendkim generated key:" \
    && cat /etc/opendkim/keys/${MAIL_TOP_DOMAIN}/default.txt

WORKDIR /data

EXPOSE 25 465 587 993 143 110 995

ENTRYPOINT [ "/usr/local/bin/entrypoint" ]

# CMD [ "tail", "-f", "/var/log/syslog" ]
