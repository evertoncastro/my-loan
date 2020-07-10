from flask import Blueprint
from flask_restplus import Api as ApiRestPlus
from api import loan as loan_namespace
api = ApiRestPlus(
    Blueprint('API de Empréstimo', __name__),
    title='Solicitação de empréstimo',
    version='1.0',
    description='Endpoints para pedido e acompanhamento de status do empréstimo'
)

loan_namespace.bind_with_api(api)


def load_api(app) -> object:
    app.register_blueprint(api.blueprint, url_prefix='/loan_api/v1.0')
    return None
