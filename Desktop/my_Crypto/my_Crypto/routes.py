from flask import render_template
from my_Crypto import app
from my_Crypto.modelos import select_all
import requests
from key import APIKEY

@app.route('/')
def index():
    tabla = select_all()

    return render_template("index.html", data = tabla, title = "Inicio")

@app.route("/purchase")



def compra():

    crypto_usadas = ("ETH", "BNB","ADA", "DOT", "BTC", "USDT", "XRP", "SOL", "MATIC")

    return render_template("compra.html", title = "Compra", crypto_usadas = crypto_usadas)

@app.route("/status")
def estado():
    return render_template("estado.html", title = "Estado", )