from app import db
from flask_restplus import Api
from flask_restplus import Namespace, Resource, fields
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import InternalServerError
from handlers.loan import CreateLoanRequest
from handlers.loan import ConsultLoanRequest


namespace = Namespace('loan', description='Loan')

create_loan_request = namespace.model(
    'Dados para solicitação de empréstimo', {
        'name': fields.String(
            description='Nome do cliente',
            required=True,
            min_length=4
        ),
        'cpf': fields.String(
            required=True,
            description='CPF do cliente',
            min_length=11, max_length=11
        ),
        'birthdate': fields.Date(
            required=True,
            description='Data de nascimento do cliente',
            pattern='0000-00-00'
        ),
        'amount': fields.Float(
            description='Valor desejado, entre R$ 1.000,00 e R$ 4.000,00',
            required=True
        ),
        'terms': fields.Integer(
            description='Quantidade de parcelas desejadas. Valores disponíveis: 6, 9 ou 12',
            required=True
        ),
        'income': fields.Float(
            description='Renda mensal do cliente',
            required=True
        )
    }
)

create_loan_response = namespace.model(
    'Resposta da solicitação de empréstimo', {
        'id': fields.String(
            required=True,
            description='UUID gerado para esta requisição'
        )
    }
)

get_loan_response = namespace.model(
    'Status do pedido', {
        'id': fields.String(
            required=True,
            description='UUID requisitado'
        ),
        'status': fields.String(
            required=True,
            description='Status atual da solicitação. Possíveis valores: processing, completed'
        ),
        'result': fields.String(
            required=True,
            description='Em caso de status completed, os valores podem ser approved ou refused, caso contrário será null'
        ),
        'refused_policy': fields.String(
            required=True,
            description='Em caso de result refused, os valores podem ser: age se foi recusado na política de idade, score na política de score ou commitment na política de comprometimento. Caso não tenha sido negado, será null'
        ),
        'amount': fields.Float(
            required=True,
            description='Montante liberado em caso de proposta aprovada. Caso contrário deve ser null'
        ),
        'terms': fields.Integer(
            required=True,
            description='Quantidade de parcelas aprovadas na oferta. Caso a proposta tenha sido recusada, deve ser null'
        )
    }
)

headers = namespace.parser()


@namespace.route('/', doc={"description": 'Cria um novo pedido de empréstimo'})
@namespace.expect(headers)
class CreateLoan(Resource):
    @namespace.response(200, 'Success')
    @namespace.response(400, 'Request Error')
    @namespace.response(500, 'Server Error')
    @namespace.expect(create_loan_request, validate=True)
    @namespace.marshal_with(create_loan_response)
    def post(self):
        session = db.session
        try:
            response = CreateLoanRequest().request(
                session, namespace.payload
            )
            session.commit()
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            raise InternalServerError(e.args[0])
        finally:
            session.close()


@namespace.route('/<string:id>', doc={"description": 'Verifica status do pedido'})
@namespace.param('id', 'Identificador do pedido')
@namespace.expect(headers)
class GetLoanStatus(Resource):
    @namespace.response(200, 'Success')
    @namespace.response(404, 'Not Found loan request')
    @namespace.response(500, 'Server Error')
    @namespace.marshal_with(get_loan_response)
    def get(self, id):
        session = db.session
        try:
            return ConsultLoanRequest().request(
                session, {"id": id}
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise InternalServerError(e.args[0])
        finally:
            session.close()


def bind_with_api(api: Api):
    api.add_namespace(namespace)
    return None
