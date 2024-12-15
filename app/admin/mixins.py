from app import app
from flask import request, redirect


class IsStaffMixin(object):
    def test_func(self):
        token = request.cookies.get('access_token', None)
        if not token:
            return False, None

        return True

    def get_redirect_url(self):
        raise NotImplementedError()

    def has_permission(self):
        return self.test_func()

    def handle_no_permission(self):
        return redirect(self.get_redirect_url())
