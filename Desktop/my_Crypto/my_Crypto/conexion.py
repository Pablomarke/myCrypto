import sqlite3
from my_Crypto import TABLE_DATA
from my_Crypto.modelos import valorCrypto

class Conexion:
    def __init__(self,
                 querySql,
                 params = []):
        self.con = sqlite3.connect(TABLE_DATA)
        self.cur = self.con.cursor()
        self.res = self.cur.execute(querySql,
                                    params)

    def select_all():
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

    def create(registroForm):
        conectarNuevo = Conexion("INSERT INTO movimientos(fecha, hora, Moneda_from, Cantidad_from, Moneda_to,Cantidad_to, valor) VALUES(?,?,?,?,?,?,?)", registroForm)
        conectarNuevo.con.commit()
        conectarNuevo.con.close()

    def euros_invertidos():
        conectarInvertidos = Conexion(f"SELECT Moneda_from, Cantidad_from  from movimientos")
        filas = conectarInvertidos.res.fetchall()
        euros = 0
        pun=0
        for i in filas:
            if filas[pun][0] == "EUR":
                euros += filas[pun][1]
            pun += 1
        conectarInvertidos.con.close()   
        return euros
    
    def euros_recuperados():
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
    
    def cryptos_usadas():
        conectarNuevo = Conexion("SELECT Moneda_to from movimientos")
        buscaCryptos = conectarNuevo.res.fetchall()
        conectarNuevo.con.close()
        cryptos_Euros = set(["EUR"])

        for i in buscaCryptos:
            print(i)
            i=str(i)
            i = i[2:5]
            cryptos_Euros.add(i)
        conectarNuevo.con.close()
        return cryptos_Euros

    def valor_actual():
        conectarInvertidos = Conexion(f"SELECT Moneda_to, Cantidad_to  from movimientos")
        crypto_inver = conectarInvertidos.res.fetchall()
        euros = 0
        pun=0
        for i in crypto_inver:
            if crypto_inver[pun][0] != "EUR":
                crypto = crypto_inver[pun][0]
                print("Nombre:", crypto)
                crypto_q = float(crypto_inver[pun][1])
                print("cantidad ",crypto_q)
                conver = valorCrypto(crypto)
                sum = conver * crypto_q
                euros += sum
            else:
                crypto = crypto_inver[pun][0]
                print("Nombre:", crypto)
                crypto_q = float(crypto_inver[pun][1])
                print("cantidad ",crypto_q)
                conver = valorCrypto(crypto)
                sum = conver * crypto_q
                euros -= sum
            pun += 1
        conectarInvertidos.con.close()   
        return euros
