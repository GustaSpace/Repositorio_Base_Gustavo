from flask import Flask, render_template, request
from datetime import datetime
import json

with open("dados.json", "r", encoding="utf-8") as arquio:
    dados = json.load(arquio)

app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def index():
    if request.method =="POST":
        nome = request.form['name']
        email = request.form['email']
        mensagem = request.form['message']

        dados_nensagem = {
            'nome' : nome,
            'email' : email,
            'mensagem' : mensagem,
            'data' : f'{datetime.today()}'

        }
        dados.append(dados_nensagem)
        with open ('dados.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)



        print(f"Nome: {nome} | Email: {email} | Mensagem: {mensagem}" )
        
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)