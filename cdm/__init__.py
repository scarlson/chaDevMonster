# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config


app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
app.debug = config.DEBUG

db = SQLAlchemy(app)

# custom jinja line delimeters
app.jinja_env.line_statement_prefix = '%'
app.jinja_env.line_comment_prefix = '##'

# register views
from cdm.views import general
app.register_blueprint(general.mod)