from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Olá, mundo!</p>"

@app.route("/sobre")
def sobre():
    return "<p>Essa aplicação tem como objetivo o aprendizado de Flask</p>"

if __name__ == "__main__":
    app.run()
