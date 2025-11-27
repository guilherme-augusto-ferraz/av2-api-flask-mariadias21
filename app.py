from flask import Flask, jsonify
from configuracao import Configuracao
from banco_dados import inicializar_banco
from routes.usuarios import bp_usuarios
from routes.livros import bp_livros

def criar_app():
    app = Flask(__name__)
    app.config.from_object(Configuracao)

    inicializar_banco(app)

    app.register_blueprint(bp_usuarios)
    app.register_blueprint(bp_livros)

    @app.route("/")
    def index():
        return jsonify({
            "mensagem": "API Biblioteca em funcionamento"
        })

    return app

if __name__ == "__main__":
    app = criar_app()
    app.run(debug=True)