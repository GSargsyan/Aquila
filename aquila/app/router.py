from flask import Blueprint, render_template, request, redirect, url_for
from app.modules.exceptions import ValidationError
from app import Players, Player

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
    return render_template('game.html', room_id=room_id)
