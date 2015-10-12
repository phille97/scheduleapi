# -*- coding: utf-8 -*-

from flask import jsonify, request
from flask_restful import reqparse, abort, Api, Resource, fields, marshal
from flask.ext.login import login_required, current_user

from ..controllers.database import get_session
from ..database.models import Apikey, User, Calendar, Event, Occasion


errors = {
    'ResourceDoesNotExist': {
        'message': "A resource with your parameters could not be found.",
        'status': 404
    },
    'LackingPermissions': {
        'message': "Authentication required",
        'status': 401,
        'extra': "Please follow the api guide to supplement apikey and apipass",
    },
    'NoDataRecived': {
        'message': "Please feed me data >:U",
        'status': 400,
        'extra': "You didn't send any data? I want data!",
    },
    'RequestThrottling': {
        'message': "Take it easy on them requests bruh",
        'status': 429,
        'extra': "",
    },
}

mfields = {
    'Calendar': {
        'id': fields.Integer,
        'name': fields.String(default=''),
        'description': fields.String(default=''),
        'color': fields.String(default=''),
        'created_at': fields.DateTime(dt_format='iso8601')
    }
}

api = Api(default_mediatype='application/json')


class Calendars(Resource):
    decorators = [login_required]

    def get(self, calendar_id):
        itm = get_session().query(Calendar).filter(User.id == current_user.id)\
                .filter(Calendar.id == calendar_id).first()
        if not itm:
            return errors['ResourceDoesNotExist'], 404
        return marshal(itm, mfields['Calendar'])

    def delete(self, calendar_id):
        session = get_session()
        itm = session.query(Calendar).filter(User.id == current_user.id)\
                .filter(Calendar.id == calendar_id).first()
        if not itm:
            return errors['ResourceDoesNotExist'], 404
        # TODO: Make dis work
        session.delete(itm)
        session.commit()
        return "Deleted", 200

    def put(self, calendar_id):
        return 'Not implemented!', 501


class CalendarList(Resource):
    decorators = [login_required]

    def get(self):
        raw_list = get_session().query(Calendar).filter(User.id == current_user.id)
        return marshal(list(raw_list), mfields['Calendar'])

    def post(self):
        session = get_session()
        calendar = Calendar()
        calendar.users.append(current_user)
        session.commit()
        return calendar, 201


class Events(Resource):
    decorators = [login_required]

    def get(self, event_id):
        return 'Not implemented!', 501

    def delete(self, event_id):
        return 'Not implemented!', 501

    def put(self, event_id):
        return 'Not implemented!', 501


class EventList(Resource):
    decorators = [login_required]

    def get(self, calendar_id):
        return 'Not implemented!', 501

    def post(self, calendar_id):
        return 'Not implemented!', 501


class Occasions(Resource):
    decorators = [login_required]

    def get(self, event_id, occasion_id):
        return 'Not implemented!', 501

    def delete(self, event_id, occasion_id):
        return 'Not implemented!', 501

    def put(self, event_id, occasion_id):
        return 'Not implemented!', 501


class OccasionList(Resource):
    decorators = [login_required]

    def get(self, event_id):
        return 'Not implemented!', 501

    def post(self, event_id):
        return 'Not implemented!', 501


api.add_resource(CalendarList, '/calendars')
api.add_resource(Calendars, '/calendars/<calendar_id>')

api.add_resource(EventList, '/calendars/<calendar_id>/events')
api.add_resource(Events, '/events/<event_id>')

api.add_resource(OccasionList, '/events/<event_id>/occasions')
api.add_resource(Occasions, '/events/<event_id>/occasions/<occasion_id>')
