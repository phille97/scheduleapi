# -*- coding: utf-8 -*-

from passlib.hash import pbkdf2_sha256
from .database import get_session
from ..database.models import User, Email

def encrypt_password(raw):
    return pbkdf2_sha256.encrypt(raw, rounds=200000, salt_size=16)

def check_password(raw, hashed):
    return pbkdf2_sha256.verify(raw, hashed)

def register(username, password, email=None):
    session = get_session()
    user = session.query(User).filter(User.username==username).first()
    if user is not None:
        return False
    # TODO: BETTER PASSWORD STORING
    new_user = User(username=username,password=encrypt_password(password))
    if email is not None:
        new_user.emails = [Email(address=email,primary=True)]
    session.add(new_user)
    session.commit()
    return True
