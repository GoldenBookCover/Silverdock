## Silverdock
A Docker environment for web development. Support PHP(Laravel) and Python(Django).

## Quickstart
If you just want a simplest setup, try this.

### .env
First get the project, I recommend you put it in a subfolder under your project
```bash
git clone https://github.com/MonstreCharmant/Silverdock.git /PATH/TO/YOUR/PROJECT/_docker
cd /PATH/TO/YOUR/PROJECT/_docker
```

Now generate an .env file from the template
```bash
cp env-example .env
```

Edit .env file and do some necessary modifications
```bash
# Edit .env with your favorite editor
PROJECT_ROOT_PATH=..  # Your project path
COMPOSE_PROJECT_NAME=my_project_name  # Docker compose namespace
COMPOSE_FILE=docker-compose.{python|php}.yml  # Your preferred compose file
DATA_PATH_HOST=my_data_path  # Database, cache, consistent file storage
PHP_VERSION=my_php_version  # MAJOR.MINOR, like 8.1
PHP_PUID=my_user_id
PHP_PGID=my_group_id
PYTHON_VERSION=my_python_version  # MAJOR.MINOR, like 3.10
WORKSPACE_BASE={python|php}  # Your preferred app language
```

If you want remote login, change ssh settings
```bash
WORKSPACE_SSH_PORT="2222"
WORKSPACE_SSH_PUBKEY="your_pubkey_content"
```

### Files

Create some config files from the templates

```bash
cd /PATH/TO/YOUR/PROJECT/_docker
cp ./conf/php/example.ini ./conf/php/workspace.ini
cp ./conf/php/example.ini ./conf/php/fpm.ini
cp ./conf/php/example.ini ./conf/php/queue.ini
cp ./conf/php-worker/supervisord.d/default.conf.example ./conf/php-worker/supervisord.d/default.conf
cp ./conf/nginx/conf.d/laravel.conf.example ./conf/nginx/conf.d/app.conf  # if you are runnig php apps
cp ./conf/nginx/conf.d/django.conf.example ./conf/nginx/conf.d/app.conf  # if you are runnig python apps
cp ./conf/redis/development.conf ./conf/redis/redis.conf
cp ./build/laravel-echo-server/development.json ./conf/laravel-echo-server/laravel-echo-server.json
```

Make sure all your `entrypoint.sh` files are in unix format, which means the end of line is `\n` instead of `\r\n`, or the containers will not start up.

```bash
dos2unix ./build/*/entrypoint.sh
```

Last but not least, modify the `.env` of your project(if existing), add database creds, etc. After you finished setup, build your project and wait until it succeeds.

```bash
docker-compose up -d
```

## TODO

- doc: mariadb: add replication, certs file, id, databases
- doc: env:PHP_FPM_LISTEN_PORT add 127.0.0.1 specifically
