from functools import wraps
from flask import request, jsonify, current_app
import jwt
from models.usuario import Usuario
from banco_dados import db
from datetime import datetime, timedelta

def gerar_token(id_usuario: int):
    payload = {
        "id_usuario": id_usuario,
        "exp": datetime.utcnow() + timedelta(seconds=current_app.config.get("JWT_EXP_DELTA_SECONDS", 3600))
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

def token_obrigatorio(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        cabecalho_auth = request.headers.get("Authorization", None)
        if not cabecalho_auth:
            return jsonify({"mensagem": "Token ausente. Cabeçalho 'Authorization: Bearer <token>' é necessário."}), 401

        partes = cabecalho_auth.split()
        if partes[0].lower() != "bearer" or len(partes) != 2:
            return jsonify({"mensagem": "Cabeçalho Authorization inválido. Use: Bearer <token>"}), 401

        token = partes[1]
        try:
            dados = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            id_usuario = dados.get("id_usuario")
            usuario = db.session.get(Usuario, id_usuario)
            if not usuario:
                return jsonify({"mensagem": "Usuário inválido."}), 401
            kwargs["usuario_atual"] = usuario
        except jwt.ExpiredSignatureError:
            return jsonify({"mensagem": "Token expirado."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"mensagem": "Token inválido."}), 401
        return f(*args, **kwargs)
    return decorada