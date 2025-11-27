from flask import Blueprint, request, jsonify
from banco_dados import db
from models.usuario import Usuario
from utils.autenticacao import gerar_token
from sqlalchemy.exc import IntegrityError

bp_usuarios = Blueprint("usuarios", __name__, url_prefix="/api/usuarios")

@bp_usuarios.route("/registrar", methods=["POST"])
def registrar():
    dados = request.get_json() or {}
    nome_usuario = dados.get("nome_usuario")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome_usuario or not email or not senha:
        return jsonify({"mensagem": "nome_usuario, email e senha são obrigatórios."}), 400

    novo_usuario = Usuario(nome_usuario=nome_usuario, email=email)
    novo_usuario.definir_senha(senha)

    try:
        db.session.add(novo_usuario)
        db.session.commit()
        return jsonify({"mensagem": "Usuário criado com sucesso.", "usuario": novo_usuario.para_dicionario()}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"mensagem": "nome_usuario ou email já existe."}), 400

@bp_usuarios.route("/login", methods=["POST"])
def login():
    dados = request.get_json() or {}
    nome_usuario = dados.get("nome_usuario")
    senha = dados.get("senha")
    
    if not nome_usuario or not senha:
        return jsonify({"mensagem": "nome_usuario e senha são obrigatórios."}), 400

    usuario = Usuario.query.filter_by(nome_usuario=nome_usuario).first()
    if usuario and usuario.checar_senha(senha):
        token = gerar_token(usuario.id)
        return jsonify({"mensagem": "Login bem-sucedido.", "token": token}), 200
    else:
        return jsonify({"mensagem": "Credenciais inválidas."}), 401

@bp_usuarios.route("/perfil", methods=["GET"])
def perfil():
    auth = request.headers.get("Authorization")
    if not auth:
        return jsonify({"mensagem": "Envie o token no header Authorization para ver o perfil."}), 401
    return jsonify({"mensagem": "Autenticação funcionando! Use /api/livros para gerenciar livros."})