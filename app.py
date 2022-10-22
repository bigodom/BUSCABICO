from datetime import date
from click import echo
from flask import Flask, render_template, request, redirect, session, flash, url_for
import psycopg2
from psycopg2 import OperationalError


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

connection = create_connection()


@app.route('/')
def principal():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return render_template('principal.html', display = 'style = display:none;')
    return render_template('principal.html')


@app.route('/index')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('cadastro')))

    trabalhador = (
    f'''
    SELECT * 
    FROM trabalhador t, oferece o
    WHERE t.fk_uemail = o.fk_temail;
    ''')
    
    try:
        trabalhador = selecao(connection, trabalhador)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    trabalho = (
        f'''
        SELECT *
        FROM trabalho
        '''
    )
    try:
        trabalho = selecao(connection, trabalho)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    endereco = (
        f'''
        SELECT endereco
        FROM trabalhador
        '''
    )
    try:
        endereco = selecao(connection, endereco)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    return render_template('index.html', titulo='Cadastrados', trabalhador=trabalhador, trabalho = trabalho, endereco = endereco)


@app.route('/index_filtro_servico', methods=['POST'])
def index_filtro_servico():


    if request.method == 'POST':
        trabalhoFiltro = request.form['trabalhoFiltro']


    trabalhador = (
    f'''
    SELECT * 
    FROM trabalhador t, oferece o
    WHERE t.fk_uemail = o.fk_temail AND o.fk_trabalhador_tipo iLIKE '{trabalhoFiltro}';
    ''')

    try:
        trabalhador = selecao(connection, trabalhador)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    trabalho = (
        f'''
        SELECT *
        FROM trabalho
        '''
    )
    try:
        trabalho = selecao(connection, trabalho)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    endereco = (
        f'''
        SELECT endereco
        FROM trabalhador
        '''
    )
    try:
        endereco = selecao(connection, endereco)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    return render_template('index.html', titulo='Cadastrados', trabalhador=trabalhador, trabalho = trabalho, endereco = endereco)


@app.route('/index_filtro_endereco', methods=['POST'])
def index_filtro_endereco():


    if request.method == 'POST':
        enderecoFiltro = request.form['enderecoFiltro']


    trabalhador = (
    f'''
    SELECT * 
    FROM trabalhador t, oferece o
    WHERE t.fk_uemail = o.fk_temail AND t.endereco iLIKE '{enderecoFiltro}';
    ''')
    try:
        trabalhador = selecao(connection, trabalhador)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    trabalho = (
        f'''
        SELECT *
        FROM trabalho
        '''
    )
    try:
        trabalho = selecao(connection, trabalho)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    endereco = (
        f'''
        SELECT endereco
        FROM trabalhador
        '''
    )
    try:
        endereco = selecao(connection, endereco)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    return render_template('index.html', titulo='Cadastrados', trabalhador=trabalhador, trabalho = trabalho, endereco = endereco)


@app.route('/index_usuario')
def index_usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('cadastro')))

    trabalhador = (
    f'''
    SELECT * 
    FROM trabalhador t, oferece o
    WHERE t.fk_uemail = o.fk_temail AND t.fk_uemail = '{session['email']}';
    ''')
    
    try:
        trabalhador = selecao(connection, trabalhador)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    trabalho = (
        f'''
        SELECT *
        FROM trabalho
        '''
    )
    try:
        trabalho = selecao(connection, trabalho)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    endereco = (
        f'''
        SELECT endereco
        FROM trabalhador
        '''
    )
    try:
        endereco = selecao(connection, endereco)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    return render_template('index.html', titulo='Cadastrados', trabalhador=trabalhador, trabalho = trabalho, endereco = endereco)


@app.route('/index_favoritos')
def index_favoritos():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('cadastro')))

    trabalhador = (
    f'''
    SELECT t.data_cadastro, t.pnome, t.unome, t.telefone, t.endereco, t.fk_uemail, o.fk_trabalhador_tipo
    FROM trabalhador t, favorita f, oferece o
    WHERE f.fk_uemail = '{session['email']}' and t.fk_uemail = f.fk_temail
    and t.fk_uemail = o.fk_temail
    ''')
    
    try:
        trabalhador = selecao(connection, trabalhador)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    trabalho = (
        f'''
        SELECT *
        FROM trabalho
        '''
    )
    try:
        trabalho = selecao(connection, trabalho)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    endereco = (
        f'''
        SELECT endereco
        FROM trabalhador
        '''
    )
    try:
        endereco = selecao(connection, endereco)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    return render_template('index.html', titulo='Cadastrados', trabalhador=trabalhador, trabalho = trabalho, endereco = endereco)


@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('cadastro')))
    return render_template('cadastro.html')


@app.route('/criar', methods=['POST', ])
def criar():

    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        trabalho = request.form['trabalho']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
    
    today = date.today()

    cadastro3 = (
        f'''
        INSERT INTO trabalho
        SELECT '{trabalho}'
        WHERE NOT EXISTS (SELECT 1 FROM trabalho WHERE tipo = '{trabalho}')
        '''
    )
    try:
        execute_query(connection, cadastro3)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')

    confereEmail = (
        f'''
        SELECT  t.fk_uemail
        FROM    trabalhador t
        WHERE   t.fk_uemail like '{session['email']}'
        '''
    )
    try:
        resultado = selecao(connection, confereEmail)
    except OperationalError as e:
        echo(f'O erro {e} ocorreu. Tente novamente.')
    if resultado:
        cadastro2 = (
        f'''
        INSERT INTO oferece
        VALUES ('{trabalho}', '{session['email']}', 'TRUE')
        '''
        )
        try:
            execute_query(connection, cadastro2)
        except OperationalError as e:
            echo(f'O erro {e} ocorreu. Tente novamente.')
        return redirect(url_for('index'))
        
    else:
        cadastroTrabalhador = (
        f'''
        INSERT INTO Trabalhador
        VALUES ('{today}', '{nome}', '{sobrenome}', '{telefone}', '{endereco}', '{session['email']}')
        '''
        ) 
        try:
            execute_query(connection, cadastroTrabalhador)
        except OperationalError as e:
            echo(f'O erro {e} ocorreu. Tente novamente.')
        cadastro2 = (
        f'''
        INSERT INTO oferece
        VALUES ('{trabalho}', '{session['email']}', 'TRUE')
        '''
        )
        try:
            execute_query(connection, cadastro2)
        except OperationalError as e:
            echo(f'O erro {e} ocorreu. Tente novamente.')
        return redirect(url_for('index'))


@app.route('/login')
def login():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        proxima = request.args.get('proxima')
        return render_template('login.html', proxima=proxima)
    
    flash('Você já está logado')
    return redirect(url_for('principal'))


@app.route('/registro')
def registro():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        proxima = request.args.get('proxima')
        return render_template('registrar.html', proxima=proxima)
    
    flash('Você está logado')
    return redirect(url_for('principal'))


@app.route('/registrar', methods=['POST', ])
def registrar():

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        confirmaSenha = request.form['confirmaSenha']

        if confirmaSenha != senha:
            flash('As senhas são diferentes. Tente novamente')
            return render_template('registrar.html')
        else:
            confereEmail = (
                f'''
                SELECT  t.fk_uemail
                FROM    trabalhador t
                WHERE   t.fk_uemail like '{email}'
                '''
                )
            try:
                resultado = selecao(connection, confereEmail)
            except OperationalError as e:
                echo(f'O erro {e} ocorreu. Tente novamente.')
            if resultado:
                echo("O email ja foi cadastrado.")
            else:
                usuario = (
                    f'''
                    INSERT INTO usuario
                    VALUES  ('{senha}','{email}')
                    '''
                )
                try:
                    execute_query(connection, usuario)
                except OperationalError as e:
                    echo(f'O erro {e} ocorreu. Tente novamente.')
                
                return render_template('login.html')

    return render_template('registro.html')

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

    consulta = (
        f'''
        SELECT  u.email
        FROM    usuario u
        WHERE   u.email like '{email}'
        AND     u.senha like '{senha}'
        '''
    )

    confere = selecao(connection, consulta)
    if confere:
        session.permanent = True
        session['email'] = email
        session['senha'] = senha
        session['usuario_logado'] = email 
        return redirect(url_for('principal'))
    else:
        flash('Email ou senha não cadastrados')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if session['usuario_logado'] == None:
        flash('Você não está logado')
        return redirect(url_for('principal'))
    else:
        session['usuario_logado'] = None
        flash('logout efetuado com sucesso')
        return redirect(url_for('principal'))

app.run(debug=True)
