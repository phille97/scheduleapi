# -*- coding: utf-8 -*-

from flask_restful import reqparse, abort, Api, Resource

errors = {
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 401,
        'extra': "",
    },
    'AuthenticationRequired': {
        'message': "",
        'status': 402,
        'extra': "",
    }
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
    def get(self, event_id, occasion_id):
        return 'Not implemented!', 501

    def delete(self, event_id, occasion_id):
        return 'Not implemented!', 501

    def put(self, event_id, occasion_id):
        return 'Not implemented!', 501


class OccasionList(Resource):
    def get(self, event_id):
        return 'Not implemented!', 501

    def post(self, event_id):
        return 'Not implemented!', 501
