import json

from flask import Blueprint, render_template, request, redirect, url_for, g, session
from app.modules.exceptions import ValidationError
from app import Players, Player, Rounds, Rooms, Bets, game_conf
from app.lib.utils import now, pp, secs_passed

router = Blueprint('router', __name__,
        template_folder='templates')

@router.route('/home')
def home():
    return render_template('home.html')

@router.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    # request.method == 'POST'
    uname = request.form['username']
    pwd = request.form['password']

    if Players.login_player(uname, pwd):
        return redirect(url_for('router.game'))
    return render_template('login.html', error='Invalid credentials')


@router.route('/register', methods=['POST'])
def register():
    uname = request.form['username']
    pwd = request.form['password']

    try:
        Players.register_player(uname, pwd)
    except ValidationError as ve:
        return render_template('login.html', error=str(ve))

    return redirect(url_for('router.home'))


@router.route('/game', methods=['GET'])
def game():
    room_id = Player.join_some_room()
    balance = Player.get_balance()
    return render_template('game.html', room_id=room_id, balance=Player.get_balance())


@router.route('/checkup', methods=['POST'])
def checkup():
    """
    status 1 -> round in progress, return time left until end
    status 2 -> player is not logged in
    status 3 -> No round running in players room
    """
    if not Player.is_logged_in():
        return json.dumps({'status': 2})

    rnd = Rounds.current_by_room_id(g.player.room_id)
    if rnd is None:
        return json.dumps({'status': 3})
    left = int(game_conf['rounds_interval']) - secs_passed(rnd.start_date)

    Players.update_by_id({'last_checkup': now()}, g.player.id)
    return json.dumps({'status': 1, 'left': int(left)})


@router.route('/bet', methods=['POST'])
def bet():
    if not Player.is_logged_in():
        return json.dumps({'status': 2})

    bets = json.loads(request.json) # bet_type: amount key values
    rnd = Rounds.current_by_room_id(g.player.room_id)
    if rnd is None:
        return json.dumps({'status': 3})

    Bets.insert_bets(bets, g.player.id, rnd.id, Player.are_bets_real())

    return json.dumps({'status': 1})

# FOR TESTING ONLY
@router.route('/logout', methods=['POST'])
def log_out():
    if 'pid' in session:
        del session['pid']
    return 'asd'
