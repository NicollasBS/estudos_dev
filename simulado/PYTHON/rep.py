import sqlite3

class Repositorio:
    def __init__(self, db_name='banco.db'):
        try:
            self.con = sqlite3.connect(db_name)
            self.cur = self.con.cursor()
            print(f"Contexão com {db_name} realizada com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise e
        
    def executar(self, sql, params = None):
        try:
            self.cur.execute(sql, params or [])
            self.con.commit()
            if sql.strip().upper().startswith('INSERT'):
                return self.cur.lastrowid
            else:
                return self.cur.rowcount
        except sqlite3.Error as e:
            print(f"Erro ao executar comando: {e}")
            self.con.rollback()
            return None
        
    def consultar(self, sql, params = None, fetch_one = False):
        try:
            self.cur.execute(sql, params or [])
            if fetch_one:
                return self.cur.fetchone()
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao executar comando: {e}")
            return None
        
    def fechar(self):
        if self.con:
            self.con.close()
            print("Conexão com o banco de dados fechada.")

# if __name__ == "__main__":
    #incicialização de uma 'migration'