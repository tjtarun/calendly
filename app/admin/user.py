from app.admin.views import BaseModelView


class UserAdminView(BaseModelView):
    can_create = True
    can_edit = True
