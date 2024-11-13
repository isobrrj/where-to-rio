# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

class Possui(db.Model):
    id_possui = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuario.id_usuario'), nullable=False)
    id_roteiro = db.Column(db.Integer, db.ForeignKey('Roteiro.id_roteiro'), nullable=False)
    preferencia = db.Column(db.String(120))

    def __repr__(self):
        return f'<Possui {self.id_usuario} - {self.id_roteiro}>'

class Feedback(db.Model):
    id_feedback = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuario.id_usuario'), nullable=False)
    id_roteiro = db.Column(db.Integer, db.ForeignKey('Roteiro.id_roteiro'), nullable=False)
    id_atracao = db.Column(db.Integer, db.ForeignKey('Atracao.id_atracao'), nullable=False)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.String(120))

    def __repr__(self):
        return f'<Feedback {self.id_usuario} - {self.id_roteiro}>'

class Roteiro(db.Model):
    id_roteiro = db.Column(db.Integer, primary_key=True)
    data-inicio = db.Column(db.Date, nullable=False)
    data-fim = db.Column(db.Date, nullable=False)
    orçamento = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Roteiro {self.nome}>'

class Tem(db.Model):
    id_tem = db.Column(db.Integer, primary_key=True)
    id_roteiro = db.Column(db.Integer, db.ForeignKey('Roteiro.id_roteiro'), nullable=False)
    id_atracao = db.Column(db.Integer, db.ForeignKey('Atracao.id_atracao'), nullable=False)

    def __repr__(self):
        return f'<Tem {self.id_roteiro} - {self.id_atracao}>'

class Atracao(db.Model):
    id_atracao = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    horario-funcionamento = db.Column(db.String(120), nullable=False)
    descrição = db.Column(db.String(120), nullable=False)
    foto = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Atracao {self.nome}>'

class Restaurante(db.Model):
    id_restaurante = db.Column(db.Integer, primary_key=True)
    id_atracao = db.Column(db.Integer, db.ForeignKey('Atracao.id_atracao'), nullable=False)
    especialidade = db.Column(db.String(120), nullable=False)
    vegetariano = db.Column(db.Boolean, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Restaurante {self.nome}>'
