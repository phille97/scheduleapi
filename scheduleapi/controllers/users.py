# -*- coding: utf-8 -*-

from .database import get_session
from ..database.models import User

def login(username, password):
    session = get_session()
    user = session.query(User).filter(User.username==username).first()
    if user is not None:
        # TODO: BETTER PASSWORD STORING
        if user.password != password or user.active == False:
            return False
        return True
    else:
        return False

def register(username, password, email=None):
    session = get_session()
    user = session.query(User).filter(User.username==username).first()
    if user is not None:
        return False
    # TODO: BETTER PASSWORD STORING
    new_user = User(username=username,password=password)
    session.add(new_user)
    session.commit()
    print("Welcome " + str(new_user))
    return True

def logout():
    pass

def getUserByApikey(apikey, apipass):
    return None

def getUserByUsername(username):
    return None