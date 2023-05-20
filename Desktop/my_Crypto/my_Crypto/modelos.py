import sqlite3
from my_Crypto import TABLE_DATA

class Conexion:
    def __init__(self,querySql,params = []):
        self.con = sqlite3.connect(TABLE_DATA)
        self.cur = self.con.cursor()
        self.res = self.cur.execute(querySql,params)

def select_all():
    
    conectar = Conexion("SELECT * from movimientos order by fecha ASC")
    filas = conectar.res.fetchall()
    columnas= conectar.res.description 
                                                          
    lista_diccionario=[]
    
    for f in filas:
        diccionario={}
        posicion=0
        for c in columnas:
            diccionario[c[0]] = f[posicion] 
            posicion +=1
        lista_diccionario.append(diccionario)

    conectar.con.close()
    return lista_diccionario

def create(registroForm):
    conectarNuevo = Conexion("INSERT INTO movimientos(fecha, hora, Moneda_from, Cantidad_from, Moneda_to,Cantidad_to) VALUES(?,?,?,?,?,?)", registroForm)
    conectarNuevo.con.commit()
    conectarNuevo.con.close()
    
