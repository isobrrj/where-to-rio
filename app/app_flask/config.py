# config.py
import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///whereto_DB.db'  # Ou qualquer URI do seu banco de dados
