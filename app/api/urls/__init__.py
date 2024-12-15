from flask import Blueprint

from app import app, AppApi
from app.api.resources import (
    UserResource,
    UsersResource,
    UserRecurringSlotsResource,
    UserSlotsResource,
    UserSlotResource,
    UserRecurringSlotResource,
    MeetingsResource,
    UserEventTypesResource,
    UserSchedulesResource,
)
from app.api.views import (
    HealthCheckView,
)

app.add_url_rule(
    "/calendly/healthcheck/", view_func=HealthCheckView.as_view("healthcheck")
)

user_blueprint = Blueprint("user_resource", __name__)
user_api = AppApi(user_blueprint)
user_api.add_resource(UserResource, "/<user_id>/")
user_api.add_resource(UsersResource, "/")

user_recurring_slot_blueprint = Blueprint("user_recurring_slot_resource", __name__)
user_recurring_slot_api = AppApi(user_recurring_slot_blueprint)
user_recurring_slot_api.add_resource(UserRecurringSlotsResource, "/")
user_recurring_slot_api.add_resource(
    UserRecurringSlotResource, "/<user_recurring_slot_id>/"
)

user_slot_blueprint = Blueprint("user_slot_resource", __name__)
user_slot_api = AppApi(user_slot_blueprint)
user_slot_api.add_resource(UserSlotsResource, "/")
user_slot_api.add_resource(UserSlotResource, "/<user_slot_id>/")

user_schedule_blueprint = Blueprint("user_schedule_resource", __name__)
user_schedule_api = AppApi(user_schedule_blueprint)
user_schedule_api.add_resource(UserSchedulesResource, "/")

user_event_type_blueprint = Blueprint("user_event_type_resource", __name__)
user_event_type_api = AppApi(user_event_type_blueprint)
user_event_type_api.add_resource(UserEventTypesResource, "/")

meeting_blueprint = Blueprint("meeting_resource", __name__)
meeting_api = AppApi(meeting_blueprint)
meeting_api.add_resource(MeetingsResource, "/")

# meeting_api.add_resource(UserSlotResource, "/<user_slot_id>/")
