from flask import render_template,request,redirect, flash
from my_Crypto import app
from my_Crypto.modelos import Base_Datos, CryptoApi
from time import strftime

#Listado de cryptomonedas permitidas por el programa
crypto_posibles = ["EUR", "ETH", "BNB","ADA", "DOT", "BTC", "USDT", "XRP", "SOL", "MATIC"]
date_select = strftime(" %d/%m/%Y")
hora_select = strftime(" %H:%M:%S")
b_d = Base_Datos()
cc = CryptoApi()

def validadorFormulario(datosFormulario):
    errores = []
    
    if datosFormulario["to_select"] == "":
        errores.append("Debes seleccionar Crypto o Moneda en to")

    if  datosFormulario["quantity"] == "" or float(datosFormulario["quantity"]) == 0:
        errores.append("Debes introducir una cantidad")

    if datosFormulario["from_select"] == "":
        errores.append("Debes seleccionar Crypto o Moneda en from")
        prueba_cantidad = b_d.cantidad_crypto()
        try:
            q_from = prueba_cantidad[datosFormulario["from_select"]]
            if float(datosFormulario["quantity"]) > float(q_from):
                errores.append("No tienes suficientes cryptomonedas")
        except:
            errores.append("Introduce tipo de cryptomoneda o moneda")
    
    return errores

# Páginas
@app.route('/')
def index():
    tabla = b_d.select_all()
    movs = len(tabla)
    b_d.cantidad_crypto()
    return render_template("index.html", 
                           data = tabla,
                           movs = movs,
                           titulo = "Tabla de movientos", 
                           title = "Inicio")

@app.route("/purchase", 
           methods = ["GET", "POST"])
def compra():
    crypto_usadas = b_d.cryptos_usadas()
    cantidades = b_d.cantidad_crypto()

    if request.method == "GET":
        return render_template("compra.html",   
                            title = "Compra", 
                            crypto_usadas = crypto_usadas,
                            crypto_posibles = crypto_posibles,
                            cantidades = cantidades,
                            pre_from = "Selecciona Euro/Cryptomoneda",
                            pre_to = "Selecciona Euro/Cryptomoneda",
                            valor = "Aquí verás el valor de Cambio",
                            pu = "Aquí verás el valor unitario",
                            q_to = "Introduce cantidad",
                            titulo = "Compra y venta de cryptomonedas"
                            )
    else:
        errores2 = validadorFormulario(request.form)
        if errores2 :
            for e2 in errores2:
                flash(e2)
            return render_template('compra.html', 
                                errores2 = errores2,
                                crypto_usadas = crypto_usadas,
                                crypto_posibles = crypto_posibles,
                                title = "Compra", 
                                valor = "Faltan datos",
                                cantidades = cantidades,
                                q_to = request.form["quantity"],
                                pre_from = request.form["from_select"],
                                pre_to = request.form["to_select"],
                                titulo = "Error en la transacción ")
       
        if request.form["Button"] == "Previsualizar":
            try:
                valor = cc.tradeoCrypto(request.form["quantity"], 
                                    request.form["from_select"],  
                                    request.form["to_select"])
                pu = cc.valorCrypto(request.form["to_select"])
                return render_template('compra.html', 
                                title = "Compra", 
                                valor = valor,
                                cantidades = cantidades,
                                q_to = request.form["quantity"],
                                pre_from = request.form["from_select"],
                                pre_to = request.form["to_select"],
                                pu = pu,
                                titulo = "Previsualización de la compra/venta"
                                )  
            except Exception as error:
                print(error)
                flash("Lo sentimos, has gastado las 100 consultas de hoy.")
                flash("Puedes seguir mirando tu base de datos.")
                return redirect("/purchase")
                        
        if request.form["Button"] == "Guardar":
            pre_from = request.form["from_select"] 
            pre_q = request.form["quantity"]
            pre_to = request.form["to_select"]
            
            try:
                if request.form["to_select"] == "EUR":
                    valor = cc.valorCrypto(pre_from)  
                else:
                    valor = cc.valorCrypto(pre_to)
            except Exception as error:
                print(error)
                flash("Lo sentimos, has gastado las 100 consultas de hoy.")
                flash("Puedes seguir mirando tu base de datos.")
                return redirect("/purchase")

            b_d.create([
                date_select,
                hora_select,
                pre_from,
                pre_q,
                pre_to,
                cc.tradeoCrypto(pre_q, 
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
    euros = b_d.euros_invertidos()
    euros_rec = b_d.euros_recuperados()
    euros_rec = round(euros_rec, 2)
    valor_compra = euros - euros_rec
    ganancia = ""
    if valor_compra >= 0:
        ganancia = "verde"
    else:
        ganancia = "rojo"

    valor_compra = round(valor_compra, 2)
    try:
        valor_act = b_d.valor_actual()
        if valor_act >= 0:
            ganancia2 = "verde"
        else:
            ganancia2 = "rojo"
    except:
            flash("Lo sentimos, has gastado las 100 consultas de hoy.")
            flash("Puedes seguir mirando tu base de datos.")
            return render_template("estado.html", 
                        title = "Estado",
                            euros = euros,
                            euros_rec = euros_rec,
                            valor_compra = valor_compra,
                            ganancia = 0,
                            valor_act = "No calculable",
                            ganancia2 = "NO",
                            ganancia3 = "NO",
                            ganancia_total = "No calculable",
                            titulo = "Estado de las transacciones"
                            )
   
    ganancia_total = valor_act - valor_compra
    if ganancia_total >= 0:
        ganancia3 = "verde"
    else:
        ganancia3 = "rojo"
    return render_template("estado.html", 
                        title = "Estado",
                            euros = euros,
                            euros_rec = euros_rec,
                            valor_compra = valor_compra,
                            ganancia = ganancia,
                            valor_act = valor_act,
                            ganancia2 = ganancia2,
                            ganancia3 = ganancia3,
                            ganancia_total = ganancia_total,
                            titulo = "Estado de las transacciones"
                            )

@app.route("/consult", 
           methods = ["GET", "POST"])
def consultar():
    if request.method == "GET":
        return render_template("consulta.html", 
                           title = "Consulta",
                           crypto_posibles = crypto_posibles,
                           comienzo = "on",
                           titulo = "Consulta valor actual cryptomonedas"
                           )
    else:
        pre_to = request.form["to_select"]
        
        try:
            valor_euro = cc.valorCrypto(pre_to)
        
        except Exception as error:
            print(error)
            flash("Lo sentimos, has gastado las 100 consultas de hoy.")
            flash("Puedes seguir mirando tu base de datos.")
            return redirect("/consult")
        
        if request.form["Button"] == "calcular":
            valor_dolar = float(valor_euro) * 1.07
            return render_template("consulta.html", 
                            title = "Consulta",
                            pre_to = pre_to,
                            valor_euro = valor_euro,
                            valor_dolar = valor_dolar,
                            crypto_posibles = crypto_posibles,
                            titulo = f"Valor actual de {pre_to}"
                            )