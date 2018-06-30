from configparser import ConfigParser

from flask import Flask, redirect, url_for, request

from app.lib.db import DB

app = Flask(__name__)

config = ConfigParser()

config.read('config.ini')
db_conf = dict(config.items('db'))
sec_conf = dict(config.items('security'))

db = DB(db_conf['host'], db_conf['user'], db_conf['pass'], db_conf['name'])

from app.modules.countries import Countries
Countries = Countries()
from app.modules.levels import Levels
Levels = Levels()
from app.modules.players import Players
Players = Players()
from app.modules.rooms import Rooms
Rooms = Rooms()
from app.modules.rounds import Rounds
Rounds = Rounds()
from app.modules.bets import Bets
Bets = Bets()
from app.router import router
app.register_blueprint(router)

from app.modules.auth import authorize

@app.before_request
def before_request():
    if not authorize():
        return redirect(url_for('login'))
