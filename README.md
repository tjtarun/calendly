## Product Overview

### Features

- User registration and login with email/OTP verification.
- JWT-based authentication with server-side token invalidation.
- Manage meetings, availability schedules, event types, custom date specific time slots, pricing, Multiple guests
- Role-based authorization for free vs. paid users.
- Book appointments with conflict handling and notification system.
- Integration with Zoom/Google Meet for video conferencing.
- Reminders and customizable notifications (push, email, WhatsApp)
- Integration with third party calendar to fetch booked slots
- Interactive automated Whatsapp Journey for users on accepting/rejecting/rescheduling/cancel

### Assumptions

- User authentication is done via email and OTP.
- Default availability and event types are pre-configured upon user registration.
- Paid users can create multiple event types, while free users are restricted to one.
- Conflict resolution is based on availability rules set by the user.
- Conflict resolution is to be checked only when second user is trying to book 1st user event slot
- A second user does not need to be registered to book a meeting but must verify their email via OTP.

### User Flow for MVP (Product Story)

#### Step 1: Registration and Login

- User visits the homepage and sees an overview of product features.
- User registers by providing an email and password, verified via an OTP.

#### Step 2: Dashboard and Availability Setup

- After login, the user is greeted with a welcome screen and pre-configured default availability and event type.
- User can edit or create a custom schedule:
    - Define availability by week, date ranges, and specific time zones.
    - Add event types with customizable durations, buffers, and assigned schedules.
    - Mark busy/unavailable times and handle exceptions for specific dates.

#### Step 3: Booking by Another User

- A second user visits the profile page of the first user and selects an event to book.
- The system checks for conflicts and either accepts or rejects the booking request.
- Upon successful booking, the second user can proceed to payment (if required).

#### Step 4: Notifications and Confirmation

- The first user receives notifications (push, email, WhatsApp) about the booking.
- The first user can confirm, reschedule, or cancel the meeting.
- Once confirmed, a video conferencing link is generated (via Zoom/Google Meet or custom integration).

#### Step 5: Meeting and Reminders

- Both users receive reminders based on configured settings.
- The meeting is tracked with metadata, and the system logs all interactions.

### MVP Metrics

#### 1. Usage Tracking:

- Percentage of users who set availability.
- Percentage of users who define date-specific hours.
- Number of event types created by users and how many have more than one.
- Number of schedules created by users.
- Number of users who get booked on their availability.
- Number of events saved due to buffer time.
- Percentage of users with different time zones.
- Number of times conflicts are encountered by second users.

#### 2. User Feedback:

- Net Promoter Score (NPS) from surveys.

#### 3. Rollout Strategy:

- Start with a small group of users or regions for phased testing.

## Technical Overview

### Tech Stack

- Backend Framework: Flask (Python)
- Database: PostgreSQL for persistent data storage
- Deployment: Hosted on render.com

### Trade-offs:

- Simplification: Using a single table user_date_slot for all date-level data.
- Avoiding foreign keys to enable future service separation (auth and scheduler).
- Opting for plain request parsing instead of dataclasses/Pydantic for development speed.

### Skipped Features:

- Notification System
- Accept/Reject of meetings
- Multiple guests
- Comprehensive testing framework

### DevOps:

- Dockerized service with production-ready setup using Gunicorn, Gevent, and Supervisor.
- CI/CD via GitHub workflows. (have skipped this, due to diminishing returns of spending more time on this assignment)

### Future Enhancements

- Recurring availability slots with overlap validation.
- Third-party integrations for calendar and conferencing tools.
- And also conflict checking from booked slots of third party calendars
- Caching mechanisms to optimize performance.
- URL shortener for user profile pages.
- Advanced analytics for product insights.
- Event-based notifications via Pub/Sub (e.g., SQS).
- Dynamic pricing models for event types and packages.
- Improved scheduling for global time zone support.
- We will have a change log/ delete log table for each patch/delete of different models and their properties, we should
  log what changed, who changed it, when they changed it.
- Extra meta data in user_slot/meeting - Description/Title of meeting etc.
- Default recurring date ranges is 1 year to be made editable for user
- Authentication - UserToken table etc.
- UserSlot API can be made better as more actions comes in
- schedule can have specific settings with it - meta data
- user_event_type can have specific settings and checks - meta data
- Sentry - Error - Monitoring tool setup
- one event can support multiple durations
- Events can have pricing attached to it
- Meetings to and fro - acceptance/reject etc.

## Database Design

### User

```
class User(BaseModelMixin):
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), default="")
```

- User Entity with some basic fields.
- Have not added password field, auth token field etc. - have skipped authentication for now

### UserSchedule

```
class UserSchedule(BaseModelMixin):
    user_id = db.Column("user_id", UUID(as_uuid=True), nullable=False, index=True)
    schedule_name = db.Column(db.String(50), nullable=False)
    schedule_code = db.Column(db.String(50), unique=True)
    __table_args__ = (
        Index(
            "ix_user_schedule_user_id_code",
            "user_id",
            "schedule_code",
            unique=True,
        ),
    )
```

- One Entity of user schedule contains multiple recurring rules.
- One user can have different schedule ie., different set of recurring rules.
- Schedule display name can be same, but code has to be unique.
- user_id,schedule code should also be unique

### UserEventType

```
class UserEventType(BaseModelMixin):
    user_id = db.Column("user_id", UUID(as_uuid=True), nullable=False, index=True)
    schedule_id = db.Column(
        "schedule_id", UUID(as_uuid=True), nullable=True, index=True
    )
    event_type = db.Column(db.String(50), nullable=False)
    code = db.Column(
        db.String(50), nullable=False
    )  # short_code / unique user event url for booking this event with the user.
    is_deleted = db.Column("is_deleted", db.Boolean, default=False, nullable=False)


    __table_args__ = (
        Index(
            "ix_user_event_type_user_id_code",
            "user_id",
            "code",
            unique=True,
        ),
    )


    def serialize(self, **kwargs):
        return {
            "id": str(self.id),
            "event_type": self.event_type,
            "is_deleted": self.is_deleted,
            "buffer_settings": self.buffer_settings,
            "available_durations": self.available_durations,
        }

```

- One user can have different types of event - for ex., 1:1, career mentoring, design discussion, interview
- These events need to have availability.
- One event type can share same type of availability.
- Event type is linked to one schedule. One schedule can be shared by multiple event types
- buffer_settings: lower_buffer, upper_buffer to keep gaps/rest for the user and avoid back to back meetings
- available_durations: contains different time of slot that can be booked by the requesting user
- available_durations pricing: for now, can also store the pricing involved for that particular event_type and duration.
  This later can be a table in itself

### UserRecurringSlot

```
class UserRecurringSlot(BaseModelMixin):
    class SlotType:
        AVAILABLE = "AVAILABLE"
        BUSY = "BUSY"


    user_id = db.Column("user_id", UUID(as_uuid=True), nullable=False, index=True)


    schedule_id = db.Column(
        "schedule_id", UUID(as_uuid=True), nullable=False, index=True
    )
    day = db.Column(db.Integer, nullable=False, default=0)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    recurring_start_date = db.Column(db.DateTime, nullable=False)
    recurring_end_date = db.Column(db.DateTime, nullable=False)


    slot_type = db.Column(
        "slot_type",
        db.String(25),
        nullable=False,
    )

```

- A recurring slot / recurring rule is one of the rule of a schedule. A schedule have multiple rules.
- Recurring slot contains which day Monday(index-0) to Sunday(index-6) the rules is for
- Recurring slot have its own recurring range. For now, hardcoded it to 2 years.
- A recurring - busy/available slot can be specified by the user by slot type

### UserSlot

```
class UserSlot(BaseModelMixin):
    class SlotType:
        AVAILABLE = "AVAILABLE"
        BUSY = "BUSY"
        MEETING = "MEETING"


    user_id = db.Column("user_id", UUID(as_uuid=True), nullable=False, index=True)
    booked_by_user_id = db.Column(
        "booked_by_user_id", UUID(as_uuid=True), nullable=True, index=True
    )


    user_event_type_id = db.Column(
        "user_event_type_id", UUID(as_uuid=True), nullable=True, index=True
    )
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    slot_type = db.Column(
        "slot_type",
        db.String(25),
        nullable=False,
    )

```

- If UserRecurringSlot is a cake mould then UserSlot is the cake
- It contains date information alongwith the time
- It allows user to specify date specific availability/busy schedule
- This table for now is also being used to track meetings booked

### Meeting / UserSlotGuest

- Meeting for now is UserSlot where slot_type=MEETING
- Have kept this as different API to have different interface with user slot and have its own set of logic while
  creating meeting
- When a meeting is booked, we also add entries to user_slot_guest

```
class UserSlotGuest(BaseModelMixin):
    guest_user_id = db.Column(
        "guest_user_id", UUID(as_uuid=True), nullable=False, index=True
    )
    guest_user_role = db.Column(
        "guest_user_role",
        db.String(25),
        nullable=False,
    )


    # state = accepted/rejected/maybe rsvp
    # guest user role can have its own setting - host, co-host, active participants, passive participants.
    # if we choose to host our own audio video or if we integrate with zoom, google meet - we pass on the information


    user_slot_id = db.Column(
        "user_slot_id", UUID(as_uuid=True), nullable=False, index=True
    )
```

## API Design
Published Documentation: https://documenter.getpostman.com/view/368207/2sAYHzF39Y
Postman workspace: https://web.postman.co/workspace/d0ec556f-97e7-41c7-91cf-cefb5ac8b992/documentation/368207-6fafde33-dcac-4cef-9cc0-74611aeb1a67

## What is supported?
- Create user
- Create user schedule
- Create user event type
- Create user recurring slot - available/busy
- Create user slot - date specific - availability
- Create meeting
- Added flask admin (without auth) for easy data viewing

## What is pending?
- Deep Testing, Basic testing has been done for conflict checking
- Edge Cases may fail or may work too

### API Sandbox
https://calendly-2gn5.onrender.com

### Running service locally
- Install docker
- Pull the image https://hub.docker.com/r/ainatarun/calendly
- Run the image: `docker run -it -p 5001:80 -e DB_PASSWORD='shared_on_email' ainatarun/calendly:latest`
- Open localhost:5001/calendly/admin in your browser
- PostgreSQL has not been setup locally, since it's available for free on render.com
