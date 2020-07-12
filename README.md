# Solicitação de Crédito


## Sobre

Projeto que simula uma API que recebe pedidos de crédito.

## Tecnologias

- Flask
- MySQL
- SQLite
- RabbitMQ
- Celery


## Ligando or serviços


## Com Docker

Com essa estrutura os serviços abaixo ficarão disponíveis:
- Flask Web server
- MySQL database
- Broker de mensagens (RabbitMQ)
- Celery (worker)


No diretório raiz do projeto execute:
```
docker-compose up --build
```

- Acesse a documentação da API em: http://0.0.0.0:8080/loan_api/v1.0/
- É possível ver os logs das tarefas assíncronas no terminal
- Acesse o painel do broker de mensagens em: http://0.0.0.0:15672/

----

## Na máquina local

Esse fluxo deve ser utilizado para desenvolvimento e testes

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

#### Iniciando o serviço da API
```
python app/main.py
```

- Acesse a documentação da API em: http://localhost:8080/loan_api/v1.0/


### Start Celery Worker
```
celery -A app.celery worker --loglevel=info
```

### Importante

- As tarefas estão sendo executadas com um delay de 7 segundos para facilitar a visualização nos testes