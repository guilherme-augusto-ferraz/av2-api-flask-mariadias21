import os

DIRETORIO_BASE = os.path.abspath(os.path.dirname(__file__))

class Configuracao:

    SECRET_KEY = os.environ.get("SECRET_KEY", "chave_super_secreta_troque_isso")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(DIRETORIO_BASE, "biblioteca.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXP_DELTA_SECONDS = 3600