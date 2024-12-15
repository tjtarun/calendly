import psycogreen.gevent

psycogreen.gevent.patch_psycopg()

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool

from app import settings


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.name = app.config["APP_NAME"]
    return app


app = create_app()


class AppApi(Api):
    def add_resource(self, resource, *urls, **kwargs):
        kwargs["strict_slashes"] = False
        if self.app is not None:
            self._register_view(self.app, resource, *urls, **kwargs)
        else:
            self.resources.append((resource, urls, kwargs))


api = AppApi(app)
db = SQLAlchemy(app, engine_options={"poolclass": NullPool})

__import__("app.models")
__import__("app.blueprint")
__import__("app.api")
__import__("app.utils")
__import__("app.admin")
