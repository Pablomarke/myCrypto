from flask import *
from my_Crypto import app

@app.route('/')
def index():
    return "esta es la pantalla de inicio"