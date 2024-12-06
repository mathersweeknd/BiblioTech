from flask import Blueprint, request, jsonify
from . import db, bcrypt
from .models import User
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__)

# Rota de registro
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')

    # Adiciona o usuário no banco de dados
    user = User(name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso!"}), 201

# Rota de login
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Busca o usuário pelo email
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Credenciais inválidas!"}), 401

    # Gera o token de acesso
    token = create_access_token(identity=user.id)
    return jsonify({"token": token}), 200
