from flask import Blueprint, render_template

router = Blueprint('router', __name__,
        template_folder='templates')


@router.route('/')
def index():
    return render_template('login.html')
