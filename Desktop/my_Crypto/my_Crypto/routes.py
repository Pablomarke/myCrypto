from flask import render_template,request,redirect, flash
from my_Crypto import app
from my_Crypto.conexion import Conexion
from my_Crypto.modelos import tradeoCrypto, valorCrypto
from time import strftime

crypto_posibles = ["EUR", "ETH", "BNB","ADA", "DOT", "BTC", "USDT", "XRP", "SOL", "MATIC"]
date_select = strftime(" %d/%m/%Y")
hora_select = strftime(" %H:%M:%S")

@app.route('/')
def index():
    tabla = Conexion.select_all()
    movs = len(tabla)
    return render_template("index.html", 
                           data = tabla,
                           movs = movs, 
                           title = "Inicio")

@app.route("/purchase", 
           methods = ["GET", "POST"])
def compra():
    crypto_usadas = Conexion.cryptos_usadas()

    valor = "Solo lectura"
    if request.method == "GET":
        return render_template("compra.html",   
                               title = "Compra", 
                               crypto_usadas = crypto_usadas,
                               crypto_posibles = crypto_posibles,
                               valor = "Aquí verás el valor de Cambio",
                               q_to = "Introduzca cantidad",
                                pre_from = "Seleccione Euro o Cryptomoneda",
                                pre_to = "Seleccione Euro o Cryptomoneda",
                               )
    else:
        if request.form["Button"] == "Previsualizar":
            
            respuesta = { 
                "pre_from" : request.form["from_select"], 
                "pre_q" : request.form["quantity"],
                "pre_to" : request.form["to_select"]
            }
            valor = tradeoCrypto(request.form["quantity"], 
                        request.form["from_select"], 
                        request.form["to_select"])
                        
            
            return render_template('compra.html', 
                                   title = "Compra", 
                                   valor = valor,
                                   q_to = request.form["quantity"],
                                   pre_from = request.form["from_select"],
                                   pre_to = request.form["to_select"]
                                   )  
        
        if request.form["Button"] == "Guardar":

            pre_from = request.form["from_select"] 
            pre_q = request.form["quantity"]
            pre_to = request.form["to_select"]
            
            if request.form["to_select"] == "EUR":
                valor = valorCrypto(pre_from)  
            else:
                valor = valorCrypto(pre_to)


            Conexion.create([
                date_select,
                hora_select,
                pre_from,
                pre_q,
                pre_to,
                tradeoCrypto(pre_q, 
                            pre_from, 
                            pre_to),
                            valor
                            ])            
            flash("Movimiento registrado correctamente!")
            return redirect('/')  
        
        else:
            return render_template("compra.html",
                                   title = "Compra",
                                   )

@app.route("/status")
def estado():
    euros = Conexion.euros_invertidos()
    euros_rec = Conexion.euros_recuperados()
    euros_rec = round(euros_rec, 2)
    valor_compra = euros - euros_rec
    valor_compra = round(valor_compra, 2)
    valor_actual = 0
    crypto_usadas = Conexion.cryptos_usadas()
    return render_template("estado.html", 
                           title = "Estado",
                            euros = euros,
                            euros_rec = euros_rec,
                            valor_compra = valor_compra,
                            valor_actual = valor_actual )