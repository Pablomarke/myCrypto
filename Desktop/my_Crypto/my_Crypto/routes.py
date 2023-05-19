from flask import render_template
from my_Crypto import app
from my_Crypto.modelos import select_all


@app.route('/')
def index():
    tabla = select_all()

    return render_template("index.html", data = tabla)

@app.route("/purchase")
def compra():
    return render_template("compra.html")

@app.route("/status")
def estado():
    return render_template("estado.html")