from app import app
from app.api.urls import (
    user_blueprint,
    user_slot_blueprint,
    user_recurring_slot_blueprint,
    meeting_blueprint,
    user_event_type_blueprint,
    user_schedule_blueprint,
)

default_url_prefix = "/calendly"

app.register_blueprint(user_blueprint, url_prefix=default_url_prefix + "/user")
app.register_blueprint(
    user_slot_blueprint, url_prefix=default_url_prefix + "/user-slot"
)
app.register_blueprint(
    user_recurring_slot_blueprint,
    url_prefix=default_url_prefix + "/user-recurring-slot",
)
app.register_blueprint(
    meeting_blueprint,
    url_prefix=default_url_prefix + "/meeting",
)

app.register_blueprint(
    user_event_type_blueprint,
    url_prefix=default_url_prefix + "/user-event-type",
)

app.register_blueprint(
    user_schedule_blueprint,
    url_prefix=default_url_prefix + "/user-schedule",
)
