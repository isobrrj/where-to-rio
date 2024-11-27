1. Acessar pasta database

2. Criar Ambiente Virtual

3. Acessar Ambiente Virtual

4. Rodar "pip install -r requirements.txt"

5. Rodar "alembic init alembic"

Migração do Banco: 

7. Rodar "alembic revision --autogenerate -m "Create tables""

8. alembic upgrade head

Agora será possível acessar o banco no dbeaver. A instância do Banco se encontra com o nome de arquivo "whereto_DB.db".