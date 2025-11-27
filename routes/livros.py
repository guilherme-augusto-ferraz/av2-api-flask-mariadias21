from flask import Blueprint, request, jsonify
from banco_dados import db
from models.livro import Livro
from utils.autenticacao import token_obrigatorio

bp_livros = Blueprint("livros", __name__, url_prefix="/api/livros")

@bp_livros.route("", methods=["POST"])
@token_obrigatorio
def criar_livro(usuario_atual):
    dados = request.get_json() or {}
    titulo = dados.get("titulo")
    autor = dados.get("autor")
    
    if not titulo or not autor:
        return jsonify({"mensagem": "titulo e autor são obrigatórios."}), 400

    novo_livro = Livro(
        titulo=titulo,
        autor=autor,
        data_publicacao=dados.get("data_publicacao"),
        isbn=dados.get("isbn"),
        descricao=dados.get("descricao"),
        id_dono=usuario_atual.id
    )
    db.session.add(novo_livro)
    db.session.commit()
    return jsonify({"mensagem": "Livro criado.", "livro": novo_livro.para_dicionario()}), 201

@bp_livros.route("", methods=["GET"])
@token_obrigatorio
def listar_livros(usuario_atual):
    livros = Livro.query.filter_by(id_dono=usuario_atual.id).all()
    return jsonify([l.para_dicionario() for l in livros]), 200

@bp_livros.route("/<int:id_livro>", methods=["GET"])
@token_obrigatorio
def obter_livro(usuario_atual, id_livro):
    livro = Livro.query.filter_by(id=id_livro, id_dono=usuario_atual.id).first()
    if not livro:
        return jsonify({"mensagem": "Livro não encontrado."}), 404
    return jsonify(livro.para_dicionario()), 200

@bp_livros.route("/<int:id_livro>", methods=["PUT"])
@token_obrigatorio
def atualizar_livro(usuario_atual, id_livro):
    livro = Livro.query.filter_by(id=id_livro, id_dono=usuario_atual.id).first()
    if not livro:
        return jsonify({"mensagem": "Livro não encontrado."}), 404
    
    dados = request.get_json() or {}
    livro.titulo = dados.get("titulo", livro.titulo)
    livro.autor = dados.get("autor", livro.autor)
    livro.data_publicacao = dados.get("data_publicacao", livro.data_publicacao)
    livro.isbn = dados.get("isbn", livro.isbn)
    livro.descricao = dados.get("descricao", livro.descricao)
    
    db.session.commit()
    return jsonify({"mensagem": "Livro atualizado.", "livro": livro.para_dicionario()}), 200

@bp_livros.route("/<int:id_livro>", methods=["DELETE"])
@token_obrigatorio
def deletar_livro(usuario_atual, id_livro):
    livro = Livro.query.filter_by(id=id_livro, id_dono=usuario_atual.id).first()
    if not livro:
        return jsonify({"mensagem": "Livro não encontrado."}), 404
    db.session.delete(livro)
    db.session.commit()
    return jsonify({"mensagem": "Livro removido."}), 200