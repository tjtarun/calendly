from app.admin.views import BaseModelView


class UserSlotAdminView(BaseModelView):
    can_create = True
    can_edit = True
    can_delete = True

