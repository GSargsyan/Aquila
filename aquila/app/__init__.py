import json
from configparser import ConfigParser
from functools import wraps

from flask import Flask, redirect, url_for, request, g, session
from uwsgidecorators import timer, postfork

from app.lib.db import DB

app = Flask(__name__)

config = ConfigParser()

config.read('config.ini')
db_conf = dict(config.items('db'))
sec_conf = dict(config.items('security'))
game_conf = dict(config.items('game'))

sec_conf['pass_rounds'] = int(sec_conf['pass_rounds'])
sec_conf['salt_size'] = int(sec_conf['salt_size'])
sec_conf['token_len'] = int(sec_conf['token_len'])

game_conf['max_anim_time'] = int(game_conf['max_anim_time'])
game_conf['rounds_interval'] = int(game_conf['rounds_interval'])
game_conf['bet_timeout'] = int(game_conf['bet_timeout'])
game_conf['player_timeout'] = int(game_conf['player_timeout'])
game_conf['initial_demo_bal'] = int(game_conf['initial_demo_bal'])


db = DB(db_conf['host'], db_conf['user'], db_conf['pass'], db_conf['name'])
app.secret_key = sec_conf['session_key']

from app.modules.countries import Countries
Countries = Countries()
from app.modules.levels import Levels
Levels = Levels()
from app.modules.logger import RoomLogger, LoginLogger
RoomLogger = RoomLogger()
LoginLogger = LoginLogger()
from app.modules.rooms import Rooms
Rooms = Rooms()
from app.modules.players import Players, Player
Players = Players()
Player = Player()
from app.modules.rounds import Rounds
Rounds = Rounds()
from app.modules.bets import Bets
Bets = Bets()


@postfork
def db_reconnect():
    global db
    db.reconnect()


@timer(2, target='mule')
def checkup_rooms(signal):
    # Remove afk players
    Players.remove_afks()

    # Run all non-empty rooms, that are not running
    Rooms.run_awaiting()

    # Close all empty rooms
    Rooms.close_empty()

    # Init new rounds in running rooms
    running = Rooms.all_running()
    for room in running:
        if not Rounds.has_room_running(room.id):
            Rounds.init_in_room(room.id)

    # End awaiting rounds
    awaiting = Rounds.awaiting_rounds()
    for rnd in awaiting:
        Rounds.end_round(rnd.id)
        Bets.commit_round_bets(rnd.id)


REQ_AUTH_URLS = ('/game')


def authorize():
    if Player.is_logged_in():
        g.player = Players.find_by_id(session['pid'])
        return True
    if request.path in REQ_AUTH_URLS:
        return False
    return True


@app.before_request
def before_request():
    if not authorize():
        return redirect(url_for('router.home'))


def pre_ajax(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not Player.is_logged_in():
            return json.dumps({'status': 2})
        return f(*args, **kwargs)
    return wrapper


from app.router import router
app.register_blueprint(router)
