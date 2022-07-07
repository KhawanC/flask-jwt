import json, bcrypt, jwt
from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '0845c4af8b444ec1b0f1153759bba690'
ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:desceproplay123@localhost/serra-flask'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(90))
    email = db.Column(db.String(120), unique=True)
    senha = db.Column(db.Text())

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
        
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return jsonify({'Alerta': 'Token inválido'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            dateJWT = datetime.strptime(payload['expiration'], '%Y-%m-%d %H:%M:%S.%f')
            if(dateJWT < datetime.now()):
                return Response(response=json.dumps({
                "status": 504,
                "mensagem": "Seu token expirou"}), status=504, mimetype='application/json')
            return Response(response=json.dumps({
                "status": 200,
                "mensagem": "Você está autenticado"}), status=200, mimetype='application/json')
        except:
            print('nao passou')
            return jsonify({'Alerta': 'Token inválido'})
    return decorated

@app.route('/auth')
@token_required
def auth():
    return 'Autenticado com sucesso'

@app.route('/cadastro', methods=['POST'])
def cadastrarUsuario():
    if request.method == 'POST':
        request_data = request.get_json()
        senha = request_data['senha'].encode('utf-8')
        hash = bcrypt.hashpw(senha, bcrypt.gensalt(10))

        if db.session.query(Usuario).filter(Usuario.email == request_data['email']).count() > 0:
            return Response(response=json.dumps({
                "status": 400,
                "mensagem": "Já existe um usuário com esse email"}), status=400, mimetype='application/json')
        
        elif len(request_data['senha']) <= 4:
            return Response(response=json.dumps({
                "status": 400,
                "mensagem": "Sua senha é muito fraca"}), status=400, mimetype='application/json')
        
        elif db.session.query(Usuario).filter(Usuario.email == request_data['email']).count() == 0:
            data = Usuario(request_data['nome'], request_data['email'], hash.decode('utf-8'))
            db.session.add(data)
            db.session.commit()
            return Response(response=json.dumps({
                "status": 201,
                "mensagem": "Usuário registrado com sucesso"}), status=201, mimetype='application/json')

@app.route('/autenticacao', methods=['POST'])
def autenticarUsuario():   
    if request.method == 'POST':
        respSenha = ''
        respNome = ''
        respId = ''
        request_data = request.get_json() 
        loginSenha = request_data['senha'].encode('utf-8')
        resp = db.session.query(Usuario).filter(Usuario.email == request_data['email'])
        for r in resp:
            respId = r.id
            respNome = r.nome
            respSenha = (r.senha).encode('utf-8')
        
        if request_data['email'] == '':
            return Response(response=json.dumps({
                "status": 400,
                "mensagem": "Seu email está vazio"}), status=400, mimetype='application/json')
        
        elif respSenha == '':
            return Response(response=json.dumps({
                "status": 400,
                "mensagem": "Não existe um usuario com esse email"}), status=400, mimetype='application/json')
        
        else :
            if bcrypt.checkpw(loginSenha, respSenha):
                token = jwt.encode({
                    'id': respId,
                    'nome': respNome,
                    'email': request_data['email'],
                    'expiration': str(datetime.now() + timedelta(minutes=30))
                },
                app.config['SECRET_KEY'], algorithm="HS256")
                return Response(response=json.dumps({
                    "status": 201,
                    "token": token}), status=201, mimetype='application/json')
            
            else :
                return Response(response=json.dumps({
                        "status": 400,
                        "mensagem": "As senhas não batem"}), status=400, mimetype='application/json')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
