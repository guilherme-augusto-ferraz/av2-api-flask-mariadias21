from banco_dados import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)

    livros = db.relationship("Livro", backref="dono", lazy=True)

    def definir_senha(self, senha: str):
        self.senha_hash = generate_password_hash(senha)

    def checar_senha(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

    def para_dicionario(self):
        return {
            "id": self.id, 
            "nome_usuario": self.nome_usuario, 
            "email": self.email
        }