from os import getenv
from app import app
from uuid import uuid1
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import NotFound
from util import validation
from datetime import datetime
from models import LoanRequestModel
from services.process_loan import async_process_loan_registry


class CreateLoanRequest:

    def request(self, session, data):
        self.validate(data)
        _id = uuid1().hex
        LoanRequestModel().create(
            session,
            id=_id,
            cpf=data['cpf'],
            name=data['name'],
            birthdate=datetime.strptime(data['birthdate'], '%Y-%m-%d'),
            amount=data['amount'],
            terms=data['terms'],
            income=data['income']
        )
        session.commit()
        app.logger.debug('Posting task')
        if getenv('FLASK_ENV') not in ['testing']:
            async_process_loan_registry.delay(_id)
        return dict(id=_id)

    def validate(self, data):
        errors = []
        if not validation.validate_cpf(data['cpf']):
            errors.append('Invalid cpf')
        if not validation.validate_date(data['birthdate']):
            errors.append('Invalid birthdate')
        if not 1000 <= data['amount'] <= 4000:
            errors.append('Invalid amount')
        if data['terms'] not in [6, 9, 12]:
            errors.append('Invalid terms')
        if len(errors) > 0:
            e = BadRequest()
            e.message = 'Invalid request'
            e.data = {'errors': errors}
            raise e


class ConsultLoanRequest:

    def request(self, session, data):
        loan_data = LoanRequestModel().fetch(
            session, data['id']
        )
        if not loan_data:
            e = NotFound()
            e.message = 'Not Found loan request'
            raise e
        return dict(
            id=loan_data.id,
            status=loan_data.status,
            result=loan_data.result,
            refused_policy=loan_data.refused_policy,
            amount=loan_data.approved_amount,
            terms=loan_data.approved_terms
        )
