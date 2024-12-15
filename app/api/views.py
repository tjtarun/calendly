from app import db
from flask import make_response, request
from flask.views import MethodView


class HealthCheckView(MethodView):
    def get(self):
        try:
            row = db.engine.execute("SELECT 1")
            if row is None:
                raise Exception("DB not accessible")
        except:
            raise Exception("DB not accessible")
        return make_response("Success 200", 200)
