from flask import Flask, render_template, request, redirect, session, flash, url_for


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
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('registro')))
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
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if '123' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Usuário não reconhecido')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('logout efetuado com sucesso')
    return redirect(url_for('index'))

app.run(debug=True)
