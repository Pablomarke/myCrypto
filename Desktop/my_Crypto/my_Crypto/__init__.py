from flask import Flask


app = Flask(__name__)

TABLE_DATA="data/movimientos.sqlite"

from my_Crypto.routes import *