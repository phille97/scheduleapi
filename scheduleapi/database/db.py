# -*- coding: utf-8 -*-

import datetime

from sqlalchemy import (
    create_engine, Sequence, Table, MetaData, Column, Integer, String, Boolean,
    Float, Text, ForeignKey, DateTime, UniqueConstraint
    )
from sqlalchemy.orm import (
    sessionmaker, mapper, relationship, backref, column_property
    )
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import RoleMixin, UserMixin
from flask.ext.login import login_user, AnonymousUserMixin

from .. import db_config


db_type = db_config['type']
allowed_db_types = ['postgresql', 'mysql', 'sqlite']

if db_type not in allowed_db_types:
    raise ValueError("Database type needs to be one of the following:"
        + ', '.join(allowed_db_types) + ". Check spelling in config!")

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

db = create_engine(DATABASE_URI)

Session = sessionmaker(bind=db)
session = Session()

from .models import Base

Base.metadata.create_all(db)