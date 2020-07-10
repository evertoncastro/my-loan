# Meu empréstimo

Todos os comando abaixo devem ser executados no diretório raiz do projeto.

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

### Definindo variáveis de ambiente
```
export PYTHONPATH=$PYTHONPATH:$(pwd)/app
export FLASK_ENV=development
export FLASK_APP=app/main.py
```

### Executando os tests
```
python tests/runner.py
```

### Iniciando a aplicação
```
flask run
```