import os
import sys

BASE_DIR = os.path.join(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from app import app as application
if __name__ == '__main__':
    application.run()
