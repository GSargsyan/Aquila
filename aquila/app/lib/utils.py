import pprint
import time                                                
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


def hash_pwd(pwd):
    return pbkdf2_sha256.using(rounds=sec_conf['pass_rounds'],
            salt_size=sec_conf['salt_size']).hash(pwd)


def verify_pwd(pwd, hashed):
    return pbkdf2_sha256.verify(pwd, hashed)


def is_latin(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    return True


def now():
    return datetime.now()


def secs_passed(d):
    return (now() - d).total_seconds()


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r (%r, %r) %2.5f sec' % (method.__name__, args, kw, te-ts))
        return result
    return timed
