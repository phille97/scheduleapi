from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from pony.orm import *

#db = Database("sqlite", "database.sqlite", create_db=True)

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    calendars = Set("Calendar")
    groups = Set("Group")
    username = Required(str, unique=True)
    password = Required(str)
    emails = Set("Email", cascade_delete=True)
    apikeys = Set("Apikey", cascade_delete=True)
    attachments = Set("Attachment")


class Group(db.Entity):
    id = PrimaryKey(int, auto=True)
    users = Set(User)
    name = Optional(str, unique=True, lazy=False)
    calendars = Set("Calendar")


class Calendar(db.Entity):
    id = PrimaryKey(int, auto=True)
    users = Set(User)
    name = Optional(str)
    events = Set("Event", cascade_delete=True)
    color = Optional(str, nullable=True)
    description = Optional(LongStr, lazy=True)
    groups = Set(Group)


class Event(db.Entity):
    id = PrimaryKey(int, auto=True)
    occasions = Set("Occasion", cascade_delete=True)
    location = Optional("Location")
    calendar = Required(Calendar)
    name = Required(str)
    description = Optional(LongStr, lazy=True)
    attachments = Set("Attachment")
    tags = Set("Tag")


class Occasion(db.Entity):
    id = PrimaryKey(int, auto=True)
    event = Required(Event)
    start = Required(datetime)
    end = Required(datetime)


class Location(db.Entity):
    id = PrimaryKey(int, auto=True)
    latitude = Optional(Decimal)
    longitude = Optional(Decimal)
    name = Required(str, nullable=True)
    event = Required(Event)


class Email(db.Entity):
    id = PrimaryKey(int, auto=True)
    address = Required(str, unique=True)
    user = Required(User)
    primary = Optional(bool, default=False)


class Apikey(db.Entity):
    id = PrimaryKey(int, auto=True)
    keyid = Required(UUID, unique=True)
    keypass = Required(str)
    user = Optional(User)
    hits = Required(int, default=0)


class Attachment(db.Entity):
    id = PrimaryKey(int, auto=True)
    upload_path = Required(str, unique=True)
    mime_type = Optional(str)
    size = Required(int)
    event = Optional(Event)
    user = Optional(User)


class Tag(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    color = Optional(str, nullable=True)
    events = Set(Event)


#sql_debug(True)
#db.generate_mapping(create_tables=True)