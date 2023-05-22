from flask import render_template,request,redirect, flash
from my_Crypto import app
from my_Crypto.conexion import Conexion
from my_Crypto.formulario import MovimientosForm
from my_Crypto.modelos import tradeoCrypto, valorCrypto
from key import APIKEY



crypto_usadas = ["EUR", "ETH", "BNB","ADA", "DOT", "BTC", "USDT", "XRP", "SOL", "MATIC"]

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
    formulario = MovimientosForm()
    
    if request.method == "GET":
        return render_template("compraPrueba.html", 
                               dataForm = formulario,  
                               title = "Compra", 
                               crypto_usadas = crypto_usadas)

    else:
        
        if formulario.validate_on_submit():
            Conexion.create([
                formulario.date_select,
                formulario.hora_select,
                formulario.from_select.data,
                formulario.quantity.data,
                formulario.to_select.data,
                tradeoCrypto(formulario.quantity.data, 
                             formulario.from_select.data, 
                             formulario.to_select.data),
                valorCrypto(formulario.to_select.data)
            ])
            
            
            flash("Movimiento registrado correactamente!!!")
            return redirect('/')  
        else:
            return render_template("compraPrueba.html",
                                   dataForm=formulario)



@app.route("/status")
def estado():
    return render_template("estado.html", 
                           title = "Estado", )