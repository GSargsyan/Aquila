from configparser import ConfigParser

from flask import Flask, redirect, url_for, request, g, session
from uwsgidecorators import timer, postfork

from app.lib.db import DB

app = Flask(__name__)

config = ConfigParser()

config.read('config.ini')
db_conf = dict(config.items('db'))
sec_conf = dict(config.items('security'))
game_conf = dict(config.items('game'))

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


@timer(2, target='mule')
def checkup_rooms(signal):
    # Remove afk players
    Players.remove_afks()

    # Run all non-empty rooms, that are not running
    awaiting = Rooms.run_awaiting()

    # Close all empty rooms
    Rooms.close_empty()

    # Init new rounds in running rooms
    running = Rooms.all_running()
    for room in running:
        if not Rounds.has_room_running(room.id):
            Rounds.init_in_room(room.id)

    # End late rounds, that didn't end
    # because a player bet request is late. 
    Rounds.end_late_rounds()


REQ_AUTH_URLS = ('/game')

def authorize():
    if 'pid' in session:
        g.player = Players.find_by_id(session['pid'])
        return True

    if request.path in REQ_AUTH_URLS:
        return False

    return True

@postfork
def db_reconnect():
    global db
    db.reconnect()

@app.before_request
def before_request():
    if not authorize():
        return redirect(url_for('router.home'))
