# -*- coding: utf-8 -*-

import datetime

from sqlalchemy import (
    Sequence, Table, MetaData, Column, Integer, String, Boolean, Float, Text,
    ForeignKey, DateTime
    )
from sqlalchemy.orm import (
    sessionmaker, mapper, relationship, backref, column_property
    )
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from flask.ext.security import RoleMixin, UserMixin
from flask.ext.login import login_user, AnonymousUserMixin

from .. import db_config


db_type = db_config['type']
allowed_db_types = ['postgresql', 'mysql', 'sqlite']

if db_type not in allowed_db_types:
    raise ValueError("""Database type needs to be one of the following:
        """ + ', '.join(allowed_db_types) + """. Check spelling in config!""")

if db_type == 'sqlite':
    DATABASE_URI = "{type}://{path}".format(
        type = db_type,
        path = db_config['sqlite']['path'])
else:
    DATABASE_URI = "{type}://{user}:{pw}@{host}/{db}".format(
        type = db_type,
        user = db_config['username'],
        pw = db_config['password'],
        host = db_config['host'],
        db = db_config['database'])

db = create_engine(DATABASE_URI,
    pool_size=20, max_overflow=10)

Session = sessionmaker(bind=db)
session = Session()

##
# Mixins
##
class Mixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

##
# Relational tables
##
users_roles = Table('users_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('role_id', Integer, ForeignKey('role.id'))# TODO
)
users_groups = Table('users_groups', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id'))# TODO
)
users_calendars = Table('users_calendars', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('role_id', Integer, ForeignKey('role.id'))# TODO
)
users_emails = Table('users_emails', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('role_id', Integer, ForeignKey('role.id'))# TODO
)
users_apikeys = Table('users_apikeys', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('role_id', Integer, ForeignKey('role.id'))# TODO
)
users_attatchments = Table('users_attatchments', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('role_id', Integer, ForeignKey('role.id'))# TODO
)
groups_calendars = Table('groups_calendars', Base.metadata,
    Column('group_id', Integer, ForeignKey('group.id')),
    Column('role_id', Integer, ForeignKey('role.id'))# TODO
)
# TODO: MOAR OF DIS


##
# Tables
##
class User(Base, Mixin, UserMixin):
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    roles = relationship('Role', secondary=users_roles,
        backref=backref('user', lazy='joined'), lazy='dynamic')
    groups = relationship('Group', secondary=users_groups,
        backref=backref('user', lazy='joined'), lazy='dynamic')
    emails = relationship('Email', secondary=users_emails,
        backref=backref('user', lazy='joined'), lazy='dynamic', cascade="all, delete-orphan")
    apikeys = relationship('Apikey', secondary=users_apikeys,
        backref=backref('user', lazy='joined'), lazy='dynamic', cascade="all, delete-orphan")
    calendars = relationship('Calendar', secondary=users_calendars,
        backref=backref('user', lazy='dynamic'))
    attatchments = relationship('Attachment', secondary=users_attatchments,
        backref=backref('user', lazy='dynamic'))

    def getOccasions(start, end):
        pass


class Role(Base, Mixin, RoleMixin):
    name = Column(String, unique=True)
    description = Column(String)


class Group(Base, Mixin):
    username = Column(String, unique=True, nullable=False)

    calendars = relationship('Calendar', secondary=groups_calendars,
        backref=backref('user', lazy='dynamic'))


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

    user = Required(User)


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
