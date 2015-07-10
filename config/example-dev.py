# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir))

APP_SECRET_KEY = 'awesome-sauce'
PORT = 5000
DEBUG = True
CLIENT_ID = 'awesome-sauce'
CLIENT_SECRET = 'awesome-sauce'
REDDIT_USERNAME = 'awesome-sauce'
REDDIT_PASSWORD = 'awesome-sauce'
DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'chadevmonster.db')