# -*- coding: utf-8 -*-

from flask_restful import reqparse, abort, Api, Resource

from .. import api_v1 as api

errors = {
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 401,
        'extra': "",
    },
}

class Calendar(Resource):
    def get(self, calendar_id):
        return 'Not implemented!', 501

    def delete(self, calendar_id):
        return 'Not implemented!', 501

    def put(self, calendar_id):
        return 'Not implemented!', 501


class CalendarList(Resource):
    def get(self):
        return 'Not implemented!', 501

    def post(self):
        return 'Not implemented!', 501


class Event(Resource):
    def get(self, event_id):
        return 'Not implemented!', 501

    def delete(self, event_id):
        return 'Not implemented!', 501

    def put(self, event_id):
        return 'Not implemented!', 501


class EventList(Resource):
    def get(self, calendar_id):
        return 'Not implemented!', 501

    def post(self, calendar_id):
        return 'Not implemented!', 501


class Occasion(Resource):
    def get(self, occasion_id):
        return 'Not implemented!', 501

    def delete(self, occasion_id):
        return 'Not implemented!', 501

    def put(self, occasion_id):
        return 'Not implemented!', 501


class OccasionList(Resource):
    def get(self, event_id):
        return 'Not implemented!', 501

    def post(self, event_id):
        return 'Not implemented!', 501


api.add_resource(CalendarList, '/calendars')
api.add_resource(Calendar, '/calendars/<calendar_id>')

api.add_resource(EventList, '/events')
api.add_resource(Event, '/events/<event_id>')

api.add_resource(OccasionList, '/events/<event_id>/occasions')
api.add_resource(Occasion, '/events/<event_id>/occasions/<occasion_id>')

