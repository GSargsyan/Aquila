from configparser import ConfigParser

from flask import Flask

from app.lib.db import DB

config = ConfigParser()
app = Flask(__name__)

config.read('config.ini')
db_conf = dict(config.items('db'))

db = DB(db_conf['host'], db_conf['user'], db_conf['pass'], db_conf['name'])

from app.models.players import Players

player = Players().find_by_id(1)
