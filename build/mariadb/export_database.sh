#!/bin/bash

databases=""

mysqldump --user=root --password="$MYSQL_ROOT_PASSWORD" \
    --master-data \
    --single-transaction \
    -R \
    --databases $databases > \
    /var/lib/mysql/all_data.sql \
    && cd /var/lib/mysql/ \
    && echo "Databases exported: $(du -sh all_data.sql)" \
    || exit 2

echo -n "Master status: "
head -n 30 /var/lib/mysql/all_data.sql | grep 'CHANGE MASTER'
sed -i '1,30s/^CHANGE MASTER/-- CHANGE MASTER/' /var/lib/mysql/all_data.sql
