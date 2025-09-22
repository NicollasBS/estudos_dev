import sqlite3
import datetime

class Logger():

    def __init__(self, matricula, evento):
        self.matricula = matricula
        self.evento = evento
        self.gdh = datetime.datetime.now()
        self.create_table()
        self.log()

    def connect(self):
        con = sqlite3.connect('banco.db')
        cur = con.cursor()
        return con, cur

    def create_table(self):
        con, cur = self.connect()
        cur.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, matricula TEXT, evento TEXT, gdh DATETIME)")
        cur.close()
        con.commit()
        con.close()

    def log(self):
        con, cur = self.connect()
        print("Salvando Log...")
        print(f"{self.matricula}, {self.evento}, {self.gdh}")
        cur.execute("INSERT INTO logs (matricula, evento, gdh) VALUES (?, ?, ?)", (self.matricula, self.evento, self.gdh))
        cur.close()
        con.commit()
        con.close()
