import logging
from json import dumps
from abc import ABC
from abc import abstractmethod
from services.customer import Customer
from util import date
from dateutil.relativedelta import relativedelta
from requests import post


class Policy(ABC):

    @abstractmethod
    def execute(self, customer: Customer) -> bool:
        pass


class AgePolicy(Policy):

    def execute(self, customer: Customer) -> bool:
        current_date = date.current_datetime()
        date_diff = relativedelta(current_date, customer.birthdate)
        if date_diff.years < 18:
            return False
        return True


class ScorePolicy(Policy):

    def execute(self, customer: Customer) -> bool:
        # TODO: trazer url ou token de um arquivo de config
        url = 'https://challenge.noverde.name/score'
        headers = {
            'x-api-key': 'SnAB7jQEFs1Ai8XtZdssa14gORT3jWPI7TWdXN97'
        }
        data = dict(cpf=customer.cpf)
        response = post(url, data=dumps(data), headers=headers)
        if response.status_code == 200:
            data = response.json()
            logging.info(data)
            if data['score'] >= 600:
                return True
            return False
        logging.critical(response.text)
        return Exception('Invalid response from score API')


class IncomeCommitmentPolicy(Policy):

    def execute(self, customer: Customer) -> bool:
        # TODO: trazer url ou token de um arquivo de config
        url = 'https://challenge.noverde.name/commitment'
        headers = {
            'x-api-key': 'SnAB7jQEFs1Ai8XtZdssa14gORT3jWPI7TWdXN97'
        }
        data = dict(cpf=customer.cpf)
        response = post(url, data=dumps(data), headers=headers)
        if response.status_code == 200:
            data = response.json()
            logging.info(data)
            return {}
        logging.critical(response.text)
        return Exception('Invalid response from score API')