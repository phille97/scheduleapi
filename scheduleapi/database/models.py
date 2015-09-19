# -*- coding: utf-8 -*-

import datetime

from sqlalchemy import (
    Sequence, Table, MetaData, Column, Integer, String, Boolean,
    Float, Text, ForeignKey, DateTime, UniqueConstraint
    )
from sqlalchemy.orm import (
    sessionmaker, mapper, relationship, backref, column_property
    )
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from flask.ext.security import RoleMixin, UserMixin
from flask.ext.login import login_user, AnonymousUserMixin

Base = declarative_base()

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
    Column('role_id', Integer, ForeignKey('role.id'))
)
users_groups = Table('users_groups', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id'))
)
users_calendars = Table('users_calendars', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('calendar_id', Integer, ForeignKey('calendar.id'))
)
users_attatchments = Table('users_attatchments', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('attachment_id', Integer, ForeignKey('attachment.id'))
)
groups_calendars = Table('groups_calendars', Base.metadata,
    Column('group_id', Integer, ForeignKey('group.id')),
    Column('calendar_id', Integer, ForeignKey('calendar.id'))
)
events_tags = Table('events_tags', Base.metadata,
    Column('event_id', Integer, ForeignKey('event.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


user_preference = Table('user_preference', Base.metadata,
    Column('pref_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("user.id"), nullable=False),
    Column('pref_name', String(40), nullable=False),
    Column('pref_value', String(100))
)


##
# Tables
##
class User(Base, Mixin, UserMixin):
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    authenticated = Column(Boolean, default=False)

    roles = relationship('Role', secondary=users_roles,
        backref=backref('user', lazy='joined'), lazy='dynamic')
    groups = relationship('Group', secondary=users_groups,
        backref=backref('user', lazy='joined'), lazy='dynamic')
    calendars = relationship('Calendar', secondary=users_calendars,
        backref=backref('user', lazy='dynamic'))
    attatchments = relationship('Attachment', secondary=users_attatchments,
        backref=backref('user', lazy='dynamic'))
    emails = relationship('Email', backref='user')
    apikeys = relationship('Apikey', backref='user')

    def is_active(self):
        return True

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Role(Base, Mixin, RoleMixin):
    name = Column(String, unique=True)
    description = Column(String)

    users = relationship('User', secondary=users_roles,
        backref=backref('role', lazy='dynamic'))

    def __repr__(self):
        return '<Role %r>' % self.name


class Group(Base, Mixin):
    name = Column(String, unique=True, nullable=False)

    users = relationship('User', secondary=users_groups,
        backref=backref('group', lazy='dynamic'))
    calendars = relationship('Calendar', secondary=groups_calendars,
        backref=backref('group', lazy='dynamic'))

    def __repr__(self):
        return '<Group %r>' % self.name


class Calendar(Base, Mixin):
    name = Column(String, nullable=True)
    description = Column(Text,  nullable=True)
    color = Column(String,  nullable=True)

    users = relationship('User', secondary=users_calendars,
        backref=backref('calendar', lazy='dynamic'))
    groups = relationship('Group', secondary=groups_calendars,
        backref=backref('calendar', lazy='dynamic'))
    events = relationship('Event', backref='calendar')

    def __repr__(self):
        return '<Calendar %r>' % self.id


class Event(Base, Mixin):
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    calendar_id = Column(Integer, ForeignKey('calendar.id'))

    attachments = relationship('Attachment', backref='event')
    tags = relationship('Tag', secondary=events_tags,
        backref=backref('event', lazy='dynamic'))
    occasions = relationship('Occasion', backref='event')
    locations = relationship('Location', backref='event')

    def __repr__(self):
        return '<Event %r>' % self.id

class Occasion(Base, Mixin):
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    event_id = Column(Integer, ForeignKey('event.id'))

    def __repr__(self):
        return '<Occasion %r>' % self.id


class Location(Base, Mixin):
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    name = Column(String, nullable=True)
    event_id = Column(Integer, ForeignKey('event.id'))

    def __repr__(self):
        return '<Location id={id}, long={id}, lat={id}>'.format(
            id=self.id,
            long=self.longitude,
            lat=self.latitude
        )


class Email(Base, Mixin):
    address = Column(String, nullable=False)
    primary = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    UniqueConstraint('address')

    def __init__(self, address, primary=False):
        self.address = address
        self.primary = primary

    def __repr__(self):
        return '<Email %r>' % self.address


class Apikey(Base, Mixin):
    keyid = Column(String, nullable=False)
    keypass = Column(String, nullable=False)
    hits = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('user.id'))

    UniqueConstraint('keyid')

    def __repr__(self):
        return '<Apikey %r>' % self.keyid


class Attachment(Base, Mixin):
    upload_path = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    event_id = Column(Integer, ForeignKey('event.id'))

    users = relationship('User', secondary=users_attatchments,
        backref=backref('attachment', lazy='dynamic'))

    UniqueConstraint('upload_path')

    def __repr__(self):
        return '<Attachment id={id}, path={path}>'.format(
            id=self.id,
            path=self.upload_path
        )


class Tag(Base, Mixin):
    name = Column(String, nullable=False)
    color = Column(String, nullable=True)

    events = relationship('Event', secondary=events_tags,
        backref=backref('tag', lazy='dynamic'))

    def __repr__(self):
        return '<Tag %r>' % self.keyid
