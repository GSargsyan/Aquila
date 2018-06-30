from flask import Blueprint, render_template, request

from app.modules.players import Players
from app.modules.bets import Bets
from app.modules.rounds import Rounds
from app.modules.rooms import Rooms

router = Blueprint('router', __name__,
        template_folder='templates')

@router.route('/')
def index():
    return 'asd' # render_template('login.html')

@router.route('/login', methods=['POST'])
def login():
    pass
