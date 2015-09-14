from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from pony.orm import *

from .. import db_config


db_type = db_config['type']

if db_type == 'postgresql':
    db = Database('postgres', user=db_config['username'], password=db_config['password'], host=db_config['host'], database=db_config['database'], create_db=True)
elif db_type == 'mysql':
    db = Database('mysql', host=db_config['host'], user=db_config['username'], passwd=db_config['password'], db=db_config['database'], create_db=True)
elif db_type == 'sqlite':
    db = Database('sqlite', db_config['sqlite']['path'], create_db=True)
else:
    db = None
    raise ValueError("""Database type needs to be one of the following:
        postgresql, mysql or sqlite. Check spelling in config!""")

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    password = Required(str)

    calendars = Set("Calendar")
    groups = Set("Group")
    emails = Set("Email", cascade_delete=True)
    apikeys = Set("Apikey", cascade_delete=True)
    attachments = Set("Attachment")

    def getOccasions(start, end):
        pass


class Group(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str, unique=True, lazy=False)

    users = Set("User")
    calendars = Set("Calendar")


class Calendar(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    description = Optional(LongStr, lazy=True)
    color = Optional(str, nullable=True)

    users = Set("User")
    groups = Set("Group")
    events = Set("Event", cascade_delete=True)

    def getNextOccasion():
        pass

    def getOccasions(start, end):
        pass

class Event(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(LongStr, lazy=True)

    location = Optional("Location")
    calendar = Required("Calendar")
    attachments = Set("Attachment")
    tags = Set("Tag")
    occasions = Set("Occasion", cascade_delete=True)

    def getNextOccasion():
        pass

    def getOccasions(start, end):
        pass


class Occasion(db.Entity):
    id = PrimaryKey(int, auto=True)
    start = Required(datetime)
    end = Required(datetime)

    event = Required(Event)


class Location(db.Entity):
    id = PrimaryKey(int, auto=True)
    latitude = Optional(Decimal)
    longitude = Optional(Decimal)
    name = Required(str, nullable=True)

    event = Required(Event)


class Email(db.Entity):
    id = PrimaryKey(int, auto=True)
    address = Required(str, unique=True)
    primary = Optional(bool, default=False)

    user = Required(User)


class Apikey(db.Entity):
    id = PrimaryKey(int, auto=True)
    keyid = Required(UUID, unique=True)
    keypass = Required(str)
    hits = Required(int, default=0)

    user = Optional(User)


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
db.generate_mapping(create_tables=True)
