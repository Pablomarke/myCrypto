import requests
from key import APIKEY
from my_Crypto.conexion import Conexion

#Funciones para trabajar con la base de datos

class Base_Datos:
    def __init__(self):
        pass

    def select_all(self):
        conectar = Conexion("SELECT * from movimientos order by fecha DESC , Hora DESC")
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

    def create(self, registroForm):
        conectarNuevo = Conexion("INSERT INTO movimientos(fecha, hora, Moneda_from, Cantidad_from, Moneda_to,Cantidad_to, valor) VALUES(?,?,?,?,?,?,?)", registroForm)
        conectarNuevo.con.commit()
        conectarNuevo.con.close()

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

#Funciones llamada API de criptomonedas

class CryptoApi:
    def __init__(self):
        pass

    def valorCrypto(self, crypto):
        url = f'https://rest.coinapi.io/v1/exchangerate/{crypto}/EUR'
        headers = {'X-CoinAPI-Key' : APIKEY}
        response = requests.get(url, 
                                headers=headers)
        r = response.json()
        rate = r["rate"]
        return rate

    def comprarCrypto(self, eur, 
                    crypto):
        rate = self.valorCrypto(crypto)
        total = eur / rate
        return total

    def tradeoCrypto(self, q, 
                    crypto,
                    crypto2):
        q = float(q)
        url = f'https://rest.coinapi.io/v1/exchangerate/{crypto2}/{crypto}'
        headers = {'X-CoinAPI-Key' : APIKEY}
        response = requests.get(url, 
                                headers=headers)
        r = response.json()
        rate = r["rate"]
        rate = float(rate)
        cambio = q/rate  
        return cambio