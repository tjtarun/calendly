from flask import url_for
from flask_admin.contrib.sqla import ModelView, form

from app.admin.mixins import IsStaffMixin


class BaseModelView(IsStaffMixin, ModelView):
    create_modal = True
    edit_modal = True
    can_delete = False
    page_size = 50
    can_edit = False
    can_view_details = True
    column_default_sort = ('created_on', True)
    column_list = []
    column_formatters = dict(state=lambda v, c, m, p: m.state)
    ignore_hidden = False
    column_filters = []
    simple_list_pager = True

    def get_redirect_url(self):
        return ''

    def is_accessible(self):
        return True

    def inaccessible_callback(self, name, **kwargs):
        return super().handle_no_permission()
