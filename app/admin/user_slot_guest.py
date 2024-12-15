from app.admin.views import BaseModelView


class UserSlotGuestAdminView(BaseModelView):
    can_create = True
    can_edit = True
    can_delete = True
