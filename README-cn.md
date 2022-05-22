## Silverdock
基于 Docker 的 web 应用开发框架。支持 PHP（Laravel）和 Python（Django）。

## 快速开始
如果你想快速开始一个项目，试试这个吧。

### .env
首先你需要获取 Silverdock 的代码，我建议你放在自己项目的一个子目录下
```bash
git clone https://github.com/MonstreCharmant/Silverdock.git /PATH/TO/YOUR/PROJECT/_docker
cd /PATH/TO/YOUR/PROJECT/_docker
```

然后创建一个 .env 文件，可以从模版复制一份
```bash
cp env-example .env
```

编辑 .env 文件，配置一些必要的选项
```bash
# Edit .env with your favorite editor
PROJECT_ROOT_PATH=..  # 你的项目路径
COMPOSE_PROJECT_NAME=my_project_name  # Docker compose 命名空间
COMPOSE_FILE=docker-compose.{python|php}.yml  # 首选 compose 文件
DATA_PATH_HOST=my_data_path  # 数据库，缓存，持久化文件挂载目录
PHP_VERSION=my_php_version  # 主板本.次版本, 例如 8.1
PHP_PUID=my_user_id
PHP_PGID=my_group_id
PYTHON_VERSION=my_python_version  # 主板本.次版本, 例如 3.10
WORKSPACE_BASE={python|php}  # 首选编程语言
```

如果你想要远程 ssh 访问，需要修改设置
```bash
WORKSPACE_SSH_PORT="2222"
WORKSPACE_SSH_PUBKEY="your_pubkey_content"
```

### 文件

创建一些配置文件，可以从模版复制
```bash
cd /PATH/TO/YOUR/PROJECT/_docker
cp ./conf/php/example.ini ./conf/php/workspace.ini
cp ./conf/php/example.ini ./conf/php/fpm.ini
cp ./conf/php/example.ini ./conf/php/queue.ini
cp ./conf/php-worker/supervisord.d/default.conf.example ./conf/php-worker/supervisord.d/default.conf
cp ./conf/nginx/conf.d/laravel.conf.example ./conf/nginx/conf.d/app.conf  # 如果你的项目是基于 php
cp ./conf/nginx/conf.d/django.conf.example ./conf/nginx/conf.d/app.conf  # 如果你的项目是基于 python
cp ./conf/redis/development.conf ./conf/redis/redis.conf
```

最后是修改你项目的 .env 文件（如果存在），添加数据库账密等信息。以上配置结束后，启动项目，等待构建结束。
```bash
docker-compose up -d
```

## TODO

- doc: mariadb: replication, certs file, id, databases
- doc: env:PHP_FPM_LISTEN_PORT add 127.0.0.1
