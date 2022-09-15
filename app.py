from mimetypes import init
from flask import Flask, render_template, request

class Cadastro:
    def __init__(self, nome, bairro, telefone):
        self.nome = nome
        self.bairro = bairro
        self.telefone = telefone

cadastro1 = Cadastro('Pedro', 'industrial', '31912341234')
lista = [cadastro1]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro')
def registro():
    return render_template('registro.html', titulo='Registro')

@app.route('/criar')
def criar():
    nome = request.form['nome']
    bairro = request.form['bairro']
    telefone = request.form['telefone']

    cadastro = Cadastro(nome, bairro, telefone)
    lista.append()

app.run()