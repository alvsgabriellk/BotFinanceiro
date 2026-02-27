from flask import Flask, request
from interpretador import interpretar_mensagem

app = Flask(__name__)


@app.route("/whatsapp")
def whatsapp():
    msg = request.args.get("msg") # args = parâmetro ; get = pega valor pelo nome
    if not msg:
        return "Nenhuma mensagem enviada", 400 # dado errado ou faltando
    resposta = interpretar_mensagem(msg)

    return resposta




if __name__ == "main":
    app.run(debug=True)