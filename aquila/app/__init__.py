from configparser import ConfigParser

from flask import Flask

from app.lib.db import DB

app = Flask(__name__)

config = ConfigParser()

config.read('config.ini')
db_conf = dict(config.items('db'))
sec_conf = dict(config.items('security'))

db = DB(db_conf['host'], db_conf['user'], db_conf['pass'], db_conf['name'])

from app.router import router
app.register_blueprint(router)

@app.before_request
def authenticate():
    pass
