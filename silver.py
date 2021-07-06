#!/usr/bin/env python3
# -*- coding: utf8 -*-

from os import getenv
from dotenv import load_dotenv

load_dotenv()

print('COMPOSE_PROJECT_NAME:', getenv('COMPOSE_PROJECT_NAME'))

