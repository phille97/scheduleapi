# -*- coding: utf-8 -*-

from flask import jsonify, request
from flask_restful import reqparse, abort, Api, Resource, fields, marshal
from flask.ext.login import login_required, current_user

from ..controllers.database import get_session
from ..database.models import Apikey, User, Calendar, Event, Occasion


errors = {
    'ResourceDoesNotExist': {
        'message': "A resource with your parameters could not be found.",
        'status': 404,
        'extra': ""
    },
    'LackingPermissions': {
        'message': "Authentication required",
        'status': 401,
        'extra': "You need the right permissions for dem data!"
    },
    'NoDataRecived': {
        'message': "Please feed me data >:U",
        'status': 400,
        'extra': "You didn't send any data? I want data!"
    },
    'RequestThrottling': {
        'message': "Take it easy on them requests bruh",
        'status': 429,
        'extra': ""
    },
}


mfields = {
    'Calendar': {
        'id': fields.Integer,
        'name': fields.String(default=''),
        'description': fields.String(default=''),
        'color': fields.String(),
        'meta': {
            'created': fields.DateTime(attribute='created_at', dt_format='iso8601'),
            'updated': fields.DateTime(attribute='updated_at', dt_format='iso8601')
        }
    },
    'Event': {
        'id': fields.Integer,
        'name': fields.String(default=''),
        'description': fields.String(default=''),
        'calendar': fields.Integer(attribute='calendar_id'),
        'meta': {
            'created': fields.DateTime(attribute='created_at', dt_format='iso8601'),
            'updated': fields.DateTime(attribute='updated_at', dt_format='iso8601')
        }
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
        itm = session.query(Calendar).filter(Calendar.id == calendar_id).first()

        if not itm:
            return errors['ResourceDoesNotExist'], 404

        if itm not in current_user.calendars:
            return errors['LackingPermissions'], 403

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
        current_user.calendars.append(calendar)
        session.commit()
        return marshal(calendar, mfields['Calendar']), 201


class Events(Resource):
    decorators = [login_required]

    def get(self, calendar_id, event_id):
        itm = get_session().query(Event).filter(User.id == current_user.id)\
                .filter(Event.id == event_id).first()
        if not itm:
            return errors['ResourceDoesNotExist'], 404
        return marshal(itm, mfields['Event'])

    def delete(self, calendar_id, event_id):
        return 'Not implemented!', 501

    def put(self, calendar_id, event_id):
        return 'Not implemented!', 501


class EventList(Resource):
    decorators = [login_required]

    def get(self, calendar_id):
        session = get_session()
        calendar = session.query(Calendar).filter(Calendar.id == calendar_id).first()
        raw_list = session.query(Event).filter(Calendar.id == calendar_id)

        if calendar not in current_user.calendars:
            return errors['LackingPermissions'], 403

        return marshal(list(raw_list), mfields['Calendar'])

    def post(self, calendar_id):
        session = get_session()
        calendar = session.query(Calendar).filter(Calendar.id == calendar_id).first()

        if calendar not in current_user.calendars:
            return errors['LackingPermissions'], 403

        event = Event()
        calendar.events.append(event)
        session.commit()
        return marshal(event, mfields['Event']), 201


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
api.add_resource(Events, '/calendars/<calendar_id>/events/<event_id>')

api.add_resource(OccasionList, '/events/<event_id>/occasions')
api.add_resource(Occasions, '/events/<event_id>/occasions/<occasion_id>')
