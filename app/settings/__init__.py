from os import environ

env = 'development'

if env == "production":
    from .production import *
elif env == "testing":
    from .testing import *
elif env == "staging":
    from .staging import *
else:
    from .local import *


POSTGRES = {
    'user': 'dbadmin',
    'pw': environ.get('DB_PASSWORD'),
    'host': 'dpg-ctdqh5lds78s739e7dd0-a.singapore-postgres.render.com',
    'port': '5432',
    'db': 'calendly_7hz7'
}

SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
