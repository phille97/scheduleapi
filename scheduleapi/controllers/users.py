# -*- coding: utf-8 -*-

import hashlib
import random

from passlib.hash import pbkdf2_sha256

from .database import get_session
from ..database.models import User, Email, Apikey


def encrypt_password(raw):
    return pbkdf2_sha256.encrypt(raw, rounds=200000, salt_size=16)


def check_password(raw, hashed):
    return pbkdf2_sha256.verify(raw, hashed)


def register(username, password, email=None):
    session = get_session()
    user = session.query(User).filter(User.username == username).first()

    if user is not None:
        return False

    new_user = User(username=username, password=encrypt_password(password))
    if email is not None:
        new_user.emails = [Email(address=email, primary=True)]

    session.add(new_user)
    session.commit()
    return True


def generate_apikey(user):
    session = get_session()
    keypass = hashlib.sha224(
        str(random.getrandbits(200)).encode('utf-8')).hexdigest()[0:35]
    keyid = str(user.id) + "-" + hashlib.sha224(str(random.getrandbits(200)
                                                    ).encode('utf-8')).hexdigest()[0:35]
    new_apikey = Apikey(keyid=keyid, keypass=keypass)
    user.apikeys.append(new_apikey)
    session.commit()
    return new_apikey


def fetch_apikeys(user):
    session = get_session()
    apikeys = session.query(Apikey).filter(Apikey.user_id == user.id)
    return apikeys


def remove_apikey(apikey):
    if apikey is not None:
        session = get_session()
        session.delete(apikey)
        session.commit()
        return True
    return False


def save_settings(form, user):
    return None
