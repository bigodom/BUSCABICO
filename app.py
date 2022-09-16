from flask import Flask, render_template, request, redirect

class Cadastro:
    def __init__(self, nome, trabalho, cidade, bairro, telefone):
        self.nome = nome
        self.trabalho = trabalho
        self.cidade = cidade
        self.bairro = bairro
        self.telefone = telefone

cadastro1 = Cadastro('Pedro', 'pedreiro', 'João Monlevade', 'industrial', '31912341234')
lista = [cadastro1]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', titulo='Cadastrados', cadastrados=lista)

@app.route('/cadastro')
def registro():
    return render_template('registro.html', titulo='Cadastro')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    trabalho = request.form['trabalho']
    cidade = request.form['cidade']
    bairro = request.form['bairro']
    telefone = request.form['telefone']

    cadastro = Cadastro(nome, trabalho, cidade, bairro, telefone)
    lista.append(cadastro)
    return redirect('/')

app.run()