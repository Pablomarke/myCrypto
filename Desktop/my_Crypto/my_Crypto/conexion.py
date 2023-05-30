import sqlite3
from my_Crypto import TABLE_DATA

class Conexion:
    def __init__(self,
                 querySql,
                 params = []):
        self.con = sqlite3.connect(TABLE_DATA)
        self.cur = self.con.cursor()
        self.res = self.cur.execute(querySql,
                                    params)

