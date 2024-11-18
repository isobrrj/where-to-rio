1. Acessar pasta app_flask

2. Criar Ambiente Virtual

3. Acessar Ambiente Virtual

4. Rodar "pip install -r requirements.txt"

5. Rodar "set FLASK_APP=app.py"

Para Criar o Banco:

6. flask db init

7. flask db migrate -m "Initial migration"

8. flask db upgrade

Agora será possível acessar o banco no dbeaver. A instância do Banco se encontra na pasta "instance" com o nome de arquivo "whereto_DB.db".