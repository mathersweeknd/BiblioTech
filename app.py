from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Facilita o acesso aos resultados como dicionário
    return conn

# Função para criar a tabela 'users' (caso não exista)
def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Chama a função para criar a tabela ao iniciar o aplicativo
create_table()

# Página de registro
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Pega os dados JSON enviados pela requisição

    # Verifica se os campos name, email e password foram passados
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    # Verifica se o email já existe no banco
    conn = get_db_connection()
    existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

    if existing_user:
        conn.close()
        return jsonify({'error': 'Email já registrado'}), 409  # 409 - Conflict (Email já existente)

    # Inserir o novo usuário no banco de dados
    conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', 
                 (name, email, password))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Registro realizado com sucesso!'}), 201

# Página de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Pega os dados JSON enviados pela requisição

    # Pega email e senha do corpo da requisição
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400

    # Verifica se o email existe no banco de dados
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()

    if user is None:
        return jsonify({'error': 'Usuário não encontrado'}), 404  # 404 - Not Found

    # Verifica se a senha está correta
    if user['password'] != password:
        return jsonify({'error': 'Senha incorreta'}), 401  # 401 - Unauthorized

    # Se o login for bem-sucedido
    return jsonify({'message': 'Login bem-sucedido!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
