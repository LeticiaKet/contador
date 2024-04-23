from flask import Flask, render_template, request, redirect, url_for, session
from usuario import Usuario  # Importar a classe Usuario do módulo usuario
from datetime import datetime, timedelta
import openpyxl

app = Flask(__name__, template_folder='paginas')
app.secret_key = 'sua_chave_secreta'  # Definir uma chave secreta para sessões
app.config['SESSION_COOKIE_NAME'] = 'session'  # Nome do cookie da sessão
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=0)  # Expirar o cookie da sessão quando o navegador for fechado  # Definir uma chave secreta para sessões

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form['cpf']
        senha = request.form['senha']

        usuario = Usuario(cpf)  # Criar uma instância de Usuario com o CPF fornecido

        if usuario.carregar_data_cadastro() and usuario.validar_senha(senha):
            session['logged_in'] = True
            session['cpf'] = cpf
            return redirect(url_for('mostrar_tempo_restante'))
        else:
            return render_template('login.html', mensagem='CPF ou senha inválidos.')

    return render_template('login.html', mensagem='')

# Rota principal para exibir o tempo restante
@app.route('/')
def mostrar_tempo_restante():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    cpf = session['cpf']
    usuario = Usuario(cpf)
    usuario.carregar_data_cadastro()
    tempo_restante = usuario.calcular_tempo_restante()
    return render_template('index.html', cpf=cpf, tempo_restante=tempo_restante)
    

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('cpf', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)