# Meu empréstimo

Todos os comandos abaixo devem ser executados no diretório raiz do projeto.

---
## Usando Docker
```
docker-compose up
```
- Acesse a documentação da API em: http://0.0.0.0:8080/loan_api/v1.0/
- Acesse o painel do broker de mensagens em: http://localhost:15672/

----

## Na máquina local

#### Preparando ambiente virtual
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

#### Instalando bibliotecas
```
pip install -r app/requirements.txt
```

#### Definindo variáveis de ambiente
```
export PYTHONPATH=$PYTHONPATH:$(pwd)/app
export FLASK_ENV=development
export FLASK_APP=app/main.py
```

#### Criação de banco e tabelas
```
flask db init --directory=development_migrations
flask db migrate --directory=development_migrations
flask db upgrade --directory=development_migrations
```

#### Executando os tests
```
export FLASK_ENV=testing
python tests/runner.py
```

#### Iniciando a aplicação
```
python app/main.py
```

- Acesse a documentação da API em: http://localhost:8080/loan_api/v1.0/


### Start Celery Worker
```
celery -A app.celery worker --loglevel=info
```

