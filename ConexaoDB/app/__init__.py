from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Inicialização do app e extensões
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configurações do Flask
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta'  # Troque por uma chave forte

    # Inicializa as extensões
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Importa e registra as rotas
    from .routes import auth
    app.register_blueprint(auth)

    return app
