from flask import Flask, render_template, request, redirect, session, flash


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
app.secret_key = 'malvadao'


@app.route('/')
def index():
    return render_template('index.html', titulo='Cadastrados', cadastrados=lista)


@app.route('/cadastro')
def registro():
    return render_template('registro.html', titulo='Cadastro')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    trabalho = request.form['trabalho']
    cidade = request.form['cidade']
    bairro = request.form['bairro']
    telefone = request.form['telefone']

    cadastro = Cadastro(nome, trabalho, cidade, bairro, telefone)
    lista.append(cadastro)
    return redirect('/')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if '123' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + ' logado com sucesso!')
        return redirect('/')
    else:
        flash('Usuário não reconhecido')
        return redirect('/login')


app.run(debug=True)
