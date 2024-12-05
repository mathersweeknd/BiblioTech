from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS  # Para permitir requisições do frontend

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # Caminho do banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa o monitoramento de modificações
app.config['JWT_SECRET_KEY'] = 'secrectkey'  # Chave secreta para criar o JWT

# Inicialização das extensões
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)  # Habilita o CORS para permitir requisições de diferentes origens

# Modelo de usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Criação das tabelas (certifique-se de que as tabelas existam)
with app.app_context():
    db.create_all()  # Cria as tabelas se não existirem

# Rota de registro
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    # Verifica se o usuário já existe
    user_exists = User.query.filter_by(username=username).first()
    if user_exists:
        return jsonify({"msg": "User already exists"}), 400

    # Criptografa a senha
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Cria o novo usuário
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    # Verifica se o usuário existe
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "Invalid username or password"}), 401

    # Verifica se a senha está correta
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid username or password"}), 401

    # Cria um token JWT
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

# Inicializando o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
