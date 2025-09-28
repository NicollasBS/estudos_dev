import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# --- CONFIGURAÇÃO INICIAL ---

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- MODELO DO BANCO DE DADOS ---

class User(db.Model):
    """
    ### ALTERADO ###
    Adicionado o campo 'nome' para ser retornado no login.
    """
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False) ### NOVO CAMPO ###
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    matricula = db.Column(db.String(6), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<User {self.matricula}>'


# --- ROTAS DA API ---

@app.route('/auth/users', methods=['POST'])
def create_user():
    """
    ### ALTERADO ###
    Agora também requer o campo 'nome' na criação do usuário.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Requisição inválida, JSON esperado."}), 400

    nome = data.get('nome') ### ALTERADO ###
    cpf = data.get('cpf')
    matricula = data.get('matricula')
    senha = data.get('senha')
    confirmacao_senha = data.get('confirmacaoSenha')

    # Validações básicas
    if not all([nome, cpf, matricula, senha, confirmacao_senha]): ### ALTERADO ###
        return jsonify({"error": "Todos os campos são obrigatórios: nome, cpf, matricula, senha, confirmacaoSenha."}), 400

    if senha != confirmacao_senha:
        return jsonify({"error": "A senha e a confirmação de senha não coincidem."}), 400

    if not (matricula and matricula.isdigit() and len(matricula) == 6):
        return jsonify({"error": "A matrícula deve conter exatamente 6 dígitos numéricos."}), 400

    if User.query.filter_by(cpf=cpf).first() is not None:
        return jsonify({"error": "Este CPF já está em uso."}), 409

    if User.query.filter_by(matricula=matricula).first() is not None:
        return jsonify({"error": "Esta matrícula já está em uso."}), 409

    hashed_password = generate_password_hash(senha, method='pbkdf2:sha256')

    # Cria o novo usuário e salva no banco
    new_user = User(nome=nome, cpf=cpf, matricula=matricula, password_hash=hashed_password) ### ALTERADO ###
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário criado com sucesso!"}), 201


@app.route('/auth/users', methods=['PATCH'])
def update_user():
    """
    ### ALTERADO ###
    Agora também permite a atualização do campo 'nome'.
    """
    data = request.get_json()

    if not data or 'matricula' not in data:
        return jsonify({"error": "O campo 'matricula' é obrigatório para identificar o usuário."}), 400

    user = User.query.filter_by(matricula=data['matricula']).first()

    if not user:
        return jsonify({"error": "Usuário não encontrado."}), 404

    ### ALTERADO: Adiciona a lógica para atualizar o nome ###
    if 'nome' in data:
        user.nome = data['nome']

    if 'cpf' in data:
        new_cpf = data['cpf']
        existing_user = User.query.filter(User.cpf == new_cpf, User.id != user.id).first()
        if existing_user:
            return jsonify({"error": "O novo CPF já está em uso por outro usuário."}), 409
        user.cpf = new_cpf

    if 'senha' in data:
        if 'confirmacaoSenha' not in data or data['senha'] != data['confirmacaoSenha']:
            return jsonify({"error": "Para atualizar a senha, 'senha' e 'confirmacaoSenha' devem ser fornecidos e devem coincidir."}), 400
        user.password_hash = generate_password_hash(data['senha'], method='pbkdf2:sha256')

    db.session.commit()

    return jsonify({"message": f"Usuário com matrícula {user.matricula} atualizado com sucesso!"}), 200


@app.route('/auth/login', methods=['POST'])
def login():
    """
    ### ALTERADO ###
    Retorna a estrutura JSON com token_access e dados do usuário no sucesso.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Requisição inválida, JSON esperado."}), 400

    matricula = data.get('matricula')
    senha = data.get('senha')

    if not matricula or not senha:
        return jsonify({"error": "Os campos 'matricula' e 'senha' são obrigatórios."}), 400

    user = User.query.filter_by(matricula=matricula).first()

    if not user or not check_password_hash(user.password_hash, senha):
        return jsonify({"error": "Matrícula ou senha inválida."}), 401

    ### ALTERADO: Constrói a resposta de sucesso com o formato solicitado ###
    response_data = {
        "token_access": "123456",  # Token estático, como solicitado
        "usuario": {
            "nome": user.nome,
            "matricula": user.matricula
        }
    }

    return jsonify(response_data), 200


# --- EXECUÇÃO DA APLICAÇÃO ---

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
