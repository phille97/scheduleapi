# -*- coding: utf-8 -*-

import datetime

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
    },
    'Occasion': {
        'id': fields.Integer,
        'event': fields.Integer(attribute='event_id'),
        'start': fields.DateTime(dt_format='iso8601'),
        'end': fields.DateTime(dt_format='iso8601'),
        'meta': {
            'created': fields.DateTime(attribute='created_at', dt_format='iso8601'),
            'updated': fields.DateTime(attribute='updated_at', dt_format='iso8601')
        }
    }
}

api = Api(default_mediatype='application/json')

base_parser = reqparse.RequestParser(bundle_errors=True)
base_parser.add_argument('page', default=1, type=int, location='args',
                         help='Page cannot be converted to int')
base_parser.add_argument('limit', default=20, type=int, location='args', 
                         help='Limit cannot be converted to int')

calen_parser = base_parser.copy()
calen_parser.add_argument('name', required=True, location=['form', 'json'],
                          help="Name cannot be blank!")
calen_parser.add_argument('description', location=['form', 'json'])
calen_parser.add_argument('color', location=['form', 'json'])

event_parser = base_parser.copy()
event_parser.add_argument('name', required=True, location=['form', 'json'],
                          help="Name cannot be blank!")
event_parser.add_argument('description', location=['form', 'json'])
event_parser.add_argument('calendar', type=int, location=['form', 'json'],
                          help='Calendar cannot be converted to int')

occas_parser = base_parser.copy()
occas_parser.add_argument('name', required=True, location=['form', 'json'],
                          help="Name cannot be blank!")
occas_parser.add_argument('description', location=['form', 'json'])
occas_parser.add_argument('event', type=int, location=['form', 'json'],
                          help='Event cannot be converted to int')
occas_parser.add_argument('start', location=['form', 'json'])
occas_parser.add_argument('end', location=['form', 'json'])


class Calendars(Resource):
    decorators = [login_required]

    def get(self, calendar_id):
        args = base_parser.parse_args()
        itm = get_session().query(Calendar).filter(Calendar.id == calendar_id).first()

        if not itm:
            return errors['ResourceDoesNotExist'], 404

        if itm not in current_user.calendars:
            return errors['LackingPermissions'], 403

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
        args = cal_parser.parse_args()
        return 'Not implemented!', 501


class CalendarList(Resource):
    decorators = [login_required]

    def get(self):
        args = base_parser.parse_args()
        raw_list = get_session().query(Calendar).filter(User.id == current_user.id)
        return marshal(list(raw_list), mfields['Calendar'])

    def post(self):
        args = cal_parser.parse_args()
        session = get_session()

        # TODO: Take, validate and set the right data
        calendar = Calendar()
        current_user.calendars.append(calendar)
        session.commit()
        return marshal(calendar, mfields['Calendar']), 201


class Events(Resource):
    decorators = [login_required]

    def get(self, calendar_id, event_id):
        args = base_parser.parse_args()
        session = get_session()
        calendar = session.query(Calendar).filter(Calendar.id == calendar_id).first()
        event = session.query(Event).filter(Event.calendar_id == calendar_id)\
                                    .filter(Event.id == event_id).first()

        if calendar not in current_user.calendars:
            return errors['LackingPermissions'], 403

        if not event:
            return errors['ResourceDoesNotExist'], 404

        return marshal(event, mfields['Event'])

    def delete(self, calendar_id, event_id):
        session = get_session()
        calendar = session.query(Calendar).filter(Calendar.id == calendar_id).first()
        event = session.query(Event).filter(Event.calendar_id == calendar_id)\
                                    .filter(Event.id == event_id).first()

        if calendar not in current_user.calendars:
            return errors['LackingPermissions'], 403
        
        if not event:
            return errors['ResourceDoesNotExist'], 404

        session.delete(event)
        session.commit()

    def put(self, calendar_id, event_id):
        args = event_parser.parse_args()
        return 'Not implemented!', 501


class EventList(Resource):
    decorators = [login_required]

    def get(self, calendar_id):
        args = base_parser.parse_args()
        session = get_session()
        calendar = session.query(Calendar).filter(Calendar.id == calendar_id).first()
        raw_list = session.query(Event).filter(Calendar.id == calendar_id)

        if not calendar:
            return errors['ResourceDoesNotExist'], 404

        if calendar not in current_user.calendars:
            return errors['LackingPermissions'], 403

        return marshal(list(raw_list), mfields['Calendar'])

    def post(self, calendar_id):
        args = event_parser.parse_args()
        session = get_session()
        calendar = session.query(Calendar).filter(Calendar.id == calendar_id).first()

        if not calendar:
            return errors['ResourceDoesNotExist'], 404

        if calendar not in current_user.calendars:
            return errors['LackingPermissions'], 403

        # TODO: Take, validate and set the right data
        event = Event()
        calendar.events.append(event)
        session.commit()
        return marshal(event, mfields['Event']), 201


class Occasions(Resource):
    decorators = [login_required]

    def get(self, calendar_id, event_id, occasion_id):
        args = base_parser.parse_args()
        return 'Not implemented!', 501

    def delete(self, calendar_id, event_id, occasion_id):
        return 'Not implemented!', 501

    def put(self, calendar_id, event_id, occasion_id):
        args = occas_parser.parse_args()
        return 'Not implemented!', 501


class OccasionList(Resource):
    decorators = [login_required]

    def get(self, calendar_id, event_id):
        args = base_parser.parse_args()
        session = get_session()
        calendar = session.query(Calendar).filter(Calendar.id == calendar_id).first()
        event = session.query(Event).filter(Event.id == event_id).first()

        if not calendar:
            return errors['ResourceDoesNotExist'], 404

        if not event:
            return errors['ResourceDoesNotExist'], 404

        if calendar not in current_user.calendars:
            return errors['LackingPermissions'], 403

        raw_list = session.query(Occasion).filter(Occasion.event_id == event_id)
        return marshal(list(raw_list), mfields['Occasion'])

    def post(self, calendar_id, event_id):
        args = occas_parser.parse_args()
        session = get_session()
        calendar = session.query(Calendar).filter(Calendar.id == calendar_id).first()
        event = session.query(Event).filter(Event.id == event_id).first()

        if not calendar:
            return errors['ResourceDoesNotExist'], 404

        if not event:
            return errors['ResourceDoesNotExist'], 404

        if calendar not in current_user.calendars:
            return errors['LackingPermissions'], 403

        occasion = Occasion(start=datetime.datetime.now(), end=datetime.datetime.now())
        event.occasions.append(occasion)
        session.commit()
        return marshal(occasion, mfields['Occasion']), 201



api.add_resource(CalendarList, '/calendars')
api.add_resource(Calendars, '/calendars/<int:calendar_id>')

api.add_resource(EventList, '/calendars/<int:calendar_id>/events')
api.add_resource(Events, '/calendars/<int:calendar_id>/events/<int:event_id>')

api.add_resource(OccasionList, '/calendars/<int:calendar_id>/events/<int:event_id>/occasions')
api.add_resource(Occasions, '/calendars/<int:calendar_id>/events/<int:event_id>/occasions/<int:occasion_id>')
