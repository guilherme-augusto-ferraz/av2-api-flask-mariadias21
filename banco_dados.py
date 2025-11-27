from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def inicializar_banco(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()