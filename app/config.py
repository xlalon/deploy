# -*- coding: utf8 -*-

import os
from dotenv import dotenv_values


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def init_config(app):
    app.config.update(dotenv_values(BASE_DIR + '/.env'))
