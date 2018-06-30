from flask import Blueprint, render_template, request
from app.modules.exceptions import ValidationError
from app import Players

router = Blueprint('router', __name__,
        template_folder='templates')

@router.route('/')
def index():
    return render_template('home.html')

@router.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@router.route('/register', methods=['POST'])
def register():
    uname = request.form['username']
    pwd = request.form['password']

    try:
        Players.register_player(uname, pwd)
    except ValidationError as ve:
        return render_template('login.html', error=str(ve))

    return render_template('home.html')
