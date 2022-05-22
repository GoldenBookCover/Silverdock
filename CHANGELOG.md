## Changelog

### 20220522
#### Add supervisord to manage and control php queues ####
If you are upgrading from a previous version, you should add these to you .env file, and build the new image `php-worker` to replace the old one `queue-worker`

- PHP_INSTALL_BCMATH=true
- PHP_INSTALL_FFMPEG=true
- PHP_INSTALL_MYSQL_CLIENT=false
- PHP_INSTALL_ZIP_ARCHIVE=true
