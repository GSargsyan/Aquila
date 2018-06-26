from configparser import ConfigParser

from flask import Flask

from app.lib.db import DB
from app.router import router

app = Flask(__name__)
app.register_blueprint(router)

config = ConfigParser()

config.read('config.ini')
db_conf = dict(config.items('db'))
sec_conf = dict(config.items('security'))

db = DB(db_conf['host'], db_conf['user'], db_conf['pass'], db_conf['name'])
