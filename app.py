from datetime import date
from click import echo
from flask import Flask, render_template, request, redirect, session, flash, url_for
import os
import psycopg2
from psycopg2 import OperationalError


# class Cadastro:
#     def __init__(self, nome, trabalho, cidade, bairro, telefone):
#         self.nome = nome
#         self.trabalho = trabalho
#         self.cidade = cidade
#         self.bairro = bairro
#         self.telefone = telefone


# class Usuario:
#     def __init__(self, nome, nickname, senha):
#         self.nome = nome
#         self.nickname = nickname
#         self.senha = senha


# usuario1 = Usuario("Pedro", 'bigodom', 'pedro123')
# usuario2 = Usuario("Guilherme", 'teste', 'teste')
# usuario3 = Usuario("Mateus", 'teste2', 'teste2')

# usuarios = {usuario1.nickname : usuario1,
#             usuario2.nickname : usuario2,
#             usuario3.nickname : usuario3 }

# cadastro1 = Cadastro('Pedro', 'pedreiro', 'João Monlevade', 'industrial', '31912341234')
# lista = [cadastro1]


app = Flask(__name__)
app.secret_key = 'malvadao'

def create_connection():
    try:
        connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="123",
            host="127.0.0.1",
            port="5432"
        )
        print("conn to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' ocurred")
    return connection

def selecao(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def execute_query (connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


@app.route('/')
def principal():
    return render_template('principal.html', titulo='homepage')


@app.route('/index')
def index():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(f'''SELECT * FROM Trabalhador;''')
    conn.commit()
    trabalhador = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', titulo='Cadastrados', trabalhador=trabalhador)


@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('cadastro')))
    return render_template('cadastro.html', titulo='Cadastro')


@app.route('/criar', methods=['POST', ])
def criar():

    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        senha = request.form['senha']
        endereco = request.form['endereco']
        email = request.form['email']
    
    today = date.today()

    cadastro = (
        f'''
        INSERT INTO Trabalhador
        VALUES ('{email}', '{today}', '{senha}', '{nome}', '{sobrenome}', '{endereco}')
        '''
    ) 
    connection = create_connection()
    try:
        execute_query(connection, cadastro)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    #cadastro = Cadastro(nome, trabalho, cidade, bairro, telefone)
    #lista.append(cadastro)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/registrar')
def registrar():

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confSenha = request.form['confSenha']

        if confSenha != senha:
            flash('As senhas são diferentes. Tente novamente')
            return render_template('registrar.html')
        else:
            usuario = (
                f'''
                Select  T.pnome
                '''
            )

    return render_template('registrar.html')

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
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
