# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Importando o Migrate
import config
from models import db  # Importando db do models para inicializar

# Criando a aplicação Flask
app = Flask(__name__)

# Carregando a configuração corretamente
app.config.from_object(config.Config)

# Inicializando o SQLAlchemy
db.init_app(app)

# Inicializando o Flask-Migrate
migrate = Migrate(app, db)

@app.route('/')
def index():
    return 'Aplicação Flask conectada ao banco de dados!'

if __name__ == '__main__':
    app.run(debug=True)
