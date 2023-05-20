from flask import Flask


app = Flask(__name__)

app.config.from_object("config")

TABLE_DATA="data/movimientos.sqlite"

from my_Crypto.routes import *