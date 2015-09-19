# -*- coding: utf-8 -*-

from flask import current_app

def get_session():
    session = getattr(current_app, 'session', None)
    if session is None:
        raise ValueError('Database session were not set!')
    return session