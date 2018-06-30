import pprint
from datetime import datetime

from passlib.hash import pbkdf2_sha256

from app import sec_conf
from app.modules.exceptions import ValidationError


def pp(obj, indent=4):
    """ Pretty printer with indents """
    p = pprint.PrettyPrinter(indent=indent)
    p.pprint(obj)


def throw(msg):
    raise Exception(msg)


def throw_ve(msg):
    raise ValidationError(msg)


def encrypt_pwd(pwd):
    return pbkdf2_sha256.encrypt(pwd, rounds=sec_conf['pass_rounds'])


def verify_pwd(pwd, encrypted):
    return pbkdf2_sha256.verify(encrypted, pwd)


def is_latin(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    return True

def now():
    return datetime.now()
