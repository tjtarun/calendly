from app import app, db
from app.models import (
    User,
    UserRecurringSlot,
    UserSlot,
    UserEventType,
    UserSlotGuest,
)
from flask_admin import Admin, AdminIndexView

from .user import UserAdminView
from .user_slot import UserSlotAdminView
from .user_recurring_slot import UserRecurringSlotAdminView
from .user_event_type import UserEventTypeAdminView
from .user_slot_guest import UserSlotGuestAdminView

admin = Admin(
    app,
    index_view=AdminIndexView(name='Home', url='/calendly/admin'),
    template_mode='bootstrap3',
    base_template='base_admin.html',
)

admin.add_view(UserAdminView(User, db.session))
admin.add_view(UserSlotAdminView(UserSlot, db.session))
admin.add_view(UserRecurringSlotAdminView(UserRecurringSlot, db.session))
admin.add_view(UserEventTypeAdminView(UserEventType, db.session))
admin.add_view(UserSlotGuestAdminView(UserSlotGuest, db.session))
