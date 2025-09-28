import requests
import re
from getpass import getpass
import sqlite3

URL_LOGIN = "http://172.32.1.75:8080/auth/login"
con = sqlite3.connect('banco.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS login(usuario, token)")

matriculaEntrada = (input("Matrícula: "))
senha = getpass("Senha: ")

re = re.match(r'^\d{6}$', matriculaEntrada)
if not re:
    print("Matrícula inválida")
    exit()

response = requests.post(URL_LOGIN, data={'matricula': str(matriculaEntrada), 'senha': str(senha)})
if response.status_code != 201:
    print("Falha na autenticação")
    exit()

json = response.json()

print(f"Bem-vindo, {json['usuario']['nome']}!")
print(f"Token: {json['access_token']}")

cur.execute("INSERT INTO login VALUES (?, ?)", (json['usuario']['nome'], json['access_token']))
con.commit()


print(cur.execute("SELECT * FROM login").fetchall())

cur.close()
con.close()
