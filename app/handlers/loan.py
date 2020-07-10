from uuid import uuid1
from werkzeug.exceptions import BadRequest
from util import validation
from datetime import datetime
from models import LoanRequestModel


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
