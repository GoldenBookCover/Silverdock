#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This script provides quick access to some docker actions

import argparse
import os
import sys
from configparser import ConfigParser
from glob import glob
from os import getenv
from pathlib import Path, PurePosixPath
from subprocess import run, Popen, PIPE
from dotenv import load_dotenv
from platform import system as platsys

#TODO: Compatible with Windows
#TODO: Query mongodb data
#TODO: mariadb cli: dcp exec mariadb mysql -u"root" -p"$MARIADB_ROOT_PASSWORD"
#TODO: mongo cli: dcp exec mongo mongo --port="$MONGODB_PORT" --username="$MONGO_ROOT_USERNAME" --password="$MONGO_ROOT_PASSWORD"
#TODO: init script: create config files and default databases

load_dotenv()
# getenv('ENV_NAME', 'default_value')
BASE_DIR = Path(__file__).resolve()


def is_in_docker() :
    try :
        with open('/proc/1/cgroup', 'r') as f:
            if ':/docker/' in f.read():
                return True
    except FileNotFoundError :
        # Windows and MAC do not have /proc/1/cgroup
        pass
    return False


def run_docker(cmd: list, tail: int=None) :
    """Run a docker-compose command"""
    if is_in_docker() :
        print('Cannot run inside docker containers')
        return 3
    dcp_exec = ['docker-compose']
    try :
        if os.getuid() > 0 :
            dcp_exec.insert(0, 'sudo')
    except AttributeError :
        # Windows does not have getuid
        pass
    if tail is None :
        return run(dcp_exec + cmd).returncode
    else :
        if platsys() == 'Windows' :
            return run(dcp_exec + cmd).returncode
        p1 = Popen(dcp_exec + cmd, stdout=PIPE)
        run(['tail', '-n', str(tail)], stdin=p1.stdout)
        return p1.returncode


def restart_php_worker() :
    """Restart php-worker processes separately."""
    if is_in_docker() :
        print('Cannot run inside docker containers')
        return 3

    for conf in glob('./conf/php-worker/supervisord.d/*.conf') :
        # Disable interpolation for process_name
        worker_config = ConfigParser(interpolation=None)
        worker_config.read(conf)

        default_section = worker_config.sections()[0]
        program_name = default_section.split(':')[1]
        numprocs = worker_config.getint(default_section, 'numprocs')
        for n in range(numprocs) :
            run_docker(['exec', 'php-worker', 'supervisorctl', 'restart', f"{program_name}:{program_name}_{n:02d}"])

    return 0


def create_database() :
    """Create databases"""
    print('Forbidden.')
    return 0
    # TODO: Should we generate .env?
    # TODO: Should we generate and apply docker-compose.local.yml?

    # TODO: Generate configs: consul/config/agent.json
    #                         laravel-echo-server/laravel-echo-server.json
    #                         ../services/canaan.json
    #                         ../services/worksheet/worksheet.json
    #                         ../services/timing/timing.json
    #                         ../services/schedule/schedule.json
    #                         nginx/sites/default.conf
    #                         php-worker/supervisord.d/default-worker.conf
    #                         php-worker/supervisord.d/workflow-worker.conf
    #                         php-worker/supervisord.d/io-worker.conf
    #                         redis/redis.conf

    # TODO: Try to generate a .sql file first, and then source it as stdin
    # TODO: same with mongo
    # docker-compose exec mariadb mysql -u"root" -p"$MARIADB_ROOT_PASSWORD"

    # Build go services
    run_go_service(['make', 'clean']) + run_go_service(['make', 'build'])
    run_docker([
        'exec',
        'mariadb',
        'mysql',
        f"--user=root",
        f"--password='{getenv('MARIADB_ROOT_PASSWORD')}'",
        '-e',
        f"CREATE DATABASE {getenv('MARIADB_DATABASE')} CHERSET utf8; "
        f"GRANT ALL ON {getenv('MARIADB_DATABASE')}.* TO {getenv('MARIADB_USER')}@'%' IDENTIFIED BY '{getenv('MARIADB_PASSWORD')}'; "
        'FLUSH PRIVILEGES;'
    ])
    # run([
    #     'exec',
    #     'mongo',
    #     'mongo',
    #     f"--authenticationDatabase=admin",
    #     f"--username='{getenv('MONGO_ROOT_USERNAME')}'",
    #     f"--password='{getenv('MONGO_ROOT_PASSWORD')}'",
    # ])


def parse_args():
    parser = argparse.ArgumentParser(description="Candock 环境辅助工具")

    parser.add_argument('--dev', '-d', action='store_true', help="进入开发环境")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--init', action='store_true', help='构建并运行所有服务')
    group.add_argument('--start', '-s', action='store_true', help='启动所有服务')
    group.add_argument('--stop', '-p', action='store_true', help="停止所有服务")
    group.add_argument('--down', action='store_true', help="停止并删除所有服务")
    group.add_argument('--restart', '-r', action='store_true', help="重启所有服务")
    group.add_argument('--restart-php', action='store_true', help="重启 php-fpm & 队列")
    group.add_argument('--restart-worker', action='store_true', help="重启队列")
    group.add_argument('--status', '-u', action='store_true', help="查看所有服务状态")
    group.add_argument('--tail', '-t', help="输出指定服务最后 50 条日志")

    parser.add_argument('--mysql', action='store_true', help="进入 mysql 命令行")
    parser.add_argument('--mongo', action='store_true', help="进入 mongo 命令行")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.dev:
        return run_docker(['exec', '-u', 'silverdock', 'workspace', 'bash'])

    if args.init:
        return run_docker(['up', '-d'])

    if args.start:
        return run_docker(['start'])

    if args.stop:
        return run_docker(['stop'])

    if args.restart:
        return run_docker(['stop']) + run_docker(['start'])

    if args.restart_worker:
        return restart_php_worker()

    if args.restart_php:
        if run_docker(['exec', '-u', 'www-data', 'php-fpm', 'php', 'artisan', 'octane:reload']) > 0 :
            return run_docker(['restart', 'php-fpm']) + restart_php_worker()
        else :
            return restart_php_worker()

    if args.down:
        return run_docker(['down'])

    if args.status:
        return run_docker(['ps'])

    if args.mysql :
        # run_docker(['exec', 'mariadb', 'mysql', '--user=root', f"--password={getenv('MARIADB_ROOT_PASSWORD')}", '-e', f"SHOW DATABASES;"])
        run_docker(['exec', 'mariadb', 'mysql', '--user=root', f"--password={getenv('MARIADB_ROOT_PASSWORD')}"])

    if args.mongo :
        run_docker(['exec', 'mongo', 'mongo', '--authenticationDatabase=admin', f"--username={getenv('MONGO_ROOT_USERNAME')}", f"--password={getenv('MONGO_ROOT_PASSWORD')}"])

    if args.tail:
        return run_docker(['logs', args.tail], tail=50)


if __name__ == "__main__":
    sys.exit(main())
