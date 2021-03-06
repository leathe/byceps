"""
byceps.config_defaults
~~~~~~~~~~~~~~~~~~~~~~

Default configuration values

:Copyright: 2006-2019 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from datetime import timedelta


# database connection
SQLALCHEMY_ECHO = False

# Disable Flask-SQLAlchemy's tracking of object modifications.
SQLALCHEMY_TRACK_MODIFICATIONS = False

# job queue
JOBS_ASYNC = True

# metrics
METRICS_ENABLED = False

# RQ dashboard (for job queue)
RQ_DASHBOARD_ENABLED = False
RQ_POLL_INTERVAL = 2500
WEB_BACKGROUND = 'white'

# login sessions
PERMANENT_SESSION_LIFETIME = timedelta(14)

# localization
LOCALE = 'de_DE.UTF-8'
LOCALES_FORMS = ['de']
TIMEZONE = 'Europe/Berlin'

# home page
ROOT_REDIRECT_TARGET = None
ROOT_REDIRECT_STATUS_CODE = 307

# shop
SHOP_ORDER_EXPORT_TIMEZONE = 'Europe/Berlin'
