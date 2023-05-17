from flask import render_template
from my_Crypto import app


@app.route('/')
def index():
    return render_template("index.html")

@app.route("/purchase")
def compra():
    return render_template("compra.html")

@app.route("/status")
def estado():
    return render_template("estado.html")