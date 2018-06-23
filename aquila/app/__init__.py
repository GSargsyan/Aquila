from flask import Flask
from configparser import ConfigParser

config = ConfigParser()
app = Flask(__name__)

config.read('config.ini')
db_conf = dict(config.items('db'))
