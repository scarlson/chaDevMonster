# -*- coding: utf-8 -*-

import os
import config
from cdm.errors import ConfigVarNotFoundError
"""Set up config variables.

If environment variable ENVIRONMENT is set to dev and the config/dev.py
file exists then use that file as config settings, otherwise pull in settings from the production environment
"""

if os.environ.get('ENVIRONMENT') == 'dev':
    try:
        import dev as config  # config/dev.py
    except:
        raise EnvironmentError('Please create config/dev.py')
else:
    # production server environment variables
    config.APP_SECRET_KEY = os.environ.get('SECRET_KEY')
    config.DEBUG = False
    config.DATABASE_URI = os.environ.get('DATABASE_URI')
    config.CLIENT_ID = os.environ.get('CLIENT_ID')
    config.PORT = os.environ.get('PORT')
    config.CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    config.REDDIT_USERNAME = os.environ.get('REDDIT_USERNAME')
    config.REDDIT_PASSWORD = os.environ.get('REDDIT_PASSWORD')


try:
    config_vars = [config.APP_SECRET_KEY, config.DATABASE_URI,
                   config.CLIENT_ID, config.CLIENT_SECRET,
                   config.REDDIT_USERNAME, config.REDDIT_PASSWORD]
    any(config_vars) is None
except Exception, e:
    missing_var = e.message.split()[-1]
    raise ConfigVarNotFoundError(missing_var)
