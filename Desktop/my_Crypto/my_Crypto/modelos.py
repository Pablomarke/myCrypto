import requests
from key import APIKEY
from my_Crypto.conexion import Conexion

# Errores
class ModelError(Exception):
    pass

#Modelo para trabajar con la base de datos

class Base_Datos:
    def __init__(self):
        pass

# Selecciona todos los movimientos
    def select_all(self):
        conectar = Conexion("SELECT * from movimientos order by ID DESC")
        filas = conectar.res.fetchall()
        columnas = conectar.res.description 
                                                            
        lista_diccionario=[]
        
        for f in filas:
            diccionario = {}
            posicion = 0
            for c in columnas:
                diccionario[c[0]] = f[posicion] 
                posicion += 1
            lista_diccionario.append(diccionario)

        conectar.con.close()
        return lista_diccionario

# Crea un nuevo registro
    def create(self, registroForm):
        conectarNuevo = Conexion("INSERT INTO movimientos(fecha, hora, Moneda_from, Cantidad_from, Moneda_to,Cantidad_to, valor) VALUES(?,?,?,?,?,?,?)", registroForm)
        conectarNuevo.con.commit()
        conectarNuevo.con.close()

# Selecciona el total de euros que hemos invertido/gastado
    def euros_invertidos(self):
        conectarInvertidos = Conexion("SELECT Moneda_from, Cantidad_from  from movimientos")
        filas = conectarInvertidos.res.fetchall()
        euros = 0
        pun=0
        for i in filas:
            if filas[pun][0] == "EUR":
                euros += filas[pun][1]
            pun += 1
        conectarInvertidos.con.close()   
        return euros

# Selecciona los euros que hemos recuperado
    def euros_recuperados(self):
        conectarInvertidos = Conexion("SELECT Moneda_to, Cantidad_to  from movimientos")
        rec = conectarInvertidos.res.fetchall()
        euros_rec = 0
        pun=0
        for i in rec:
            if rec[pun][0] == "EUR":
                euros_rec += rec[pun][1]
            pun += 1
        conectarInvertidos.con.close()   
        return euros_rec

#Selecciona las cryptos que hemos comprado
    def cryptos_usadas(self):
        conectarNuevo = Conexion("SELECT Moneda_to from movimientos")
        buscaCryptos = conectarNuevo.res.fetchall()
        conectarNuevo.con.close()
        cryptos_Euros = set(["EUR"])
        for i in buscaCryptos:
            i=str(i)
            i = i[2:5]
            cryptos_Euros.add(i)
        conectarNuevo.con.close()
        return cryptos_Euros

# Calcula el valor actual de las cryptomonedas compradas
    def valor_actual(self):
        conectarInvertidos = Conexion("SELECT Moneda_to, Cantidad_to  from movimientos")
        crypto_inver = conectarInvertidos.res.fetchall()
        euros = 0
        pun=0
        for i in crypto_inver:
            crypto_coin= CryptoApi()
            if crypto_inver[pun][0] != "EUR":
                crypto = crypto_inver[pun][0]
                crypto_q = float(crypto_inver[pun][1])
                conver = crypto_coin.valorCrypto(crypto)
                sum = conver * crypto_q
                euros += sum
            else:
                crypto = crypto_inver[pun][0]
                crypto_q = float(crypto_inver[pun][1])
                conver = crypto_coin.valorCrypto(crypto)
                sum = conver * crypto_q
                euros -= sum
            pun += 1
        conectarInvertidos.con.close()   
        return euros

# Selecciona cantidad de una moneda en concreto
    def cantidad_crypto(self):
        conectarCantidad = Conexion("SELECT Moneda_to, Cantidad_to  from movimientos")
        cryptos = conectarCantidad.res.fetchall()
        dicc = {}
        for i in cryptos:
            if i[0] not in dicc:
                dicc[i[0]] = i[1]
            else:
                dicc[i[0]] += i[1]
        return dicc

#Modelo llamada a la API de criptomonedas y control de errores



class CryptoApi:
    def __init__(self):
        pass

# Calcular valor respecto al euro
    def valorCrypto(self, crypto):
        url = f'https://rest.coinapi.io/v1/exchangerate/{crypto}/EUR'
        headers = {'X-CoinAPI-Key' : APIKEY}
        response = requests.get(url, 
                                headers=headers)
        r = response.json()
        if response.status_code != 200:
            print(f"status: {response.status_code}, error: {r['error']}")
            raise Exception("Error en consulta codigo de error:{}".format(response.status_code))
        else:
            r = response.json()
            rate = r["rate"]
            return rate

# Calcular la el valor en cryptos de la compra en euros
    def comprarCrypto(self, eur, 
                    crypto):
        rate = self.valorCrypto(crypto)
        total = eur / rate
        return total

# calcular el valor de la crytpo o moneda respecto a otra
    def tradeoCrypto(self, q, 
                    crypto,
                    crypto2):
        q = float(q)
        url = f'https://rest.coinapi.io/v1/exchangerate/{crypto2}/{crypto}'
        headers = {'X-CoinAPI-Key' : APIKEY}
        response = requests.get(url, 
                                headers=headers)
        r = response.json()
        if response.status_code != 200:
            print(f"status: {response.status_code}, error: {r['error']}")
            raise Exception("Error en consulta codigo de error:{}".format(response.status_code))
            
        else:
            rate = r["rate"]
            rate = float(rate)
            cambio = q/rate  
            return cambio