from banco_dados import db

class Livro(db.Model):
    __tablename__ = "livros"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(120), nullable=False)
    data_publicacao = db.Column(db.String(30), nullable=True)
    isbn = db.Column(db.String(50), nullable=True)
    descricao = db.Column(db.Text, nullable=True)

    id_dono = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    def para_dicionario(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "data_publicacao": self.data_publicacao,
            "isbn": self.isbn,
            "descricao": self.descricao,
            "id_dono": self.id_dono
        }