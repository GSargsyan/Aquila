from configparser import ConfigParser

from flask import Flask, redirect, url_for, request, g, session
from uwsgidecorators import timer

from app.lib.db import DB

app = Flask(__name__)

config = ConfigParser()

config.read('config.ini')
db_conf = dict(config.items('db'))
sec_conf = dict(config.items('security'))

db = DB(db_conf['host'], db_conf['user'], db_conf['pass'], db_conf['name'])
app.secret_key = sec_conf['session_key']

from app.modules.countries import Countries
Countries = Countries()
from app.modules.levels import Levels
Levels = Levels()
from app.modules.logger import RoomLogger, ActionLogger
RoomLogger = RoomLogger()
from app.modules.rooms import Rooms
Rooms = Rooms()
from app.modules.players import Players, Player
Players = Players()
Player = Player()
from app.modules.rounds import Rounds
Rounds = Rounds()
from app.modules.bets import Bets
Bets = Bets()
from app.router import router
app.register_blueprint(router)

@timer(5, target='mule')
def check_afk_players(signal):
    Players.remove_afks()

REQ_AUTH_URLS = ('/game')

def authorize():
    if 'pid' in session:
        g.player = Players.find_by_id(session['pid'])
        return True

    if request.path in REQ_AUTH_URLS:
        return False

    return True

@app.before_request
def before_request():
    if not authorize():
        return redirect(url_for('router.home'))
