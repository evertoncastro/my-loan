import logging
from app import app
from json import dumps
from abc import ABC
from abc import abstractmethod
from entities import Customer
from util import date
from dateutil.relativedelta import relativedelta
from requests import post
from services.term_tax import ScoreTermTaxes
from services.term_tax import TermTaxes
from services.loan import TermCalc
from services.loan import IncomeCommitment


class Policy(ABC):

    @abstractmethod
    def execute(self, customer: Customer) -> bool:
        pass


class AgePolicy(Policy):

    def execute(self, customer: Customer) -> bool:
        current_date = date.current_datetime()
        date_diff = relativedelta(current_date, customer.birthdate)
        if date_diff.years < 18:
            customer.loan_request.result = 'refused'
            customer.loan_request.refused_policy = 'age'
            return False
        return True


class ScorePolicy(Policy):

    def execute(self, customer: Customer) -> bool:
        url = f'{app.config["LOAN_API_URL"]}/score'
        headers = {
            'x-api-key': app.config["LOAN_API_TOKEN"]
        }
        data = dict(cpf=customer.cpf)
        response = post(url, data=dumps(data), headers=headers)
        if response.status_code == 200:
            data = response.json()
            logging.info(data)
            if data['score'] >= 600:
                customer.loan_request.score = data['score']
                return True
            customer.loan_request.result = 'refused'
            customer.loan_request.refused_policy = 'score'
            return False
        logging.critical(response.text)
        return Exception('Invalid response from score API')


class IncomeCommitmentPolicy(Policy):

    def execute(self, customer: Customer) -> bool:
        url = f'{app.config["LOAN_API_URL"]}/commitment'
        headers = {
            'x-api-key': app.config["LOAN_API_TOKEN"]
        }
        data = dict(cpf=customer.cpf)
        response = post(url, data=dumps(data), headers=headers)
        if response.status_code == 200:
            data = response.json()
            customer.loan_request.commitment = data['commitment']
            return self.check_given_loan(customer)
        logging.critical(response.text)
        return Exception('Invalid response from score API')

    def check_given_loan(self, customer: Customer):
        term_taxes = ScoreTermTaxes().get_by_score(
            customer.loan_request.score
        )
        term_to_try = customer.loan_request.given_term
        while term_to_try is not None:
            available = self.check_available_loan_term(
                customer, term_taxes
            )
            if not available:
                term_to_try = term_taxes.get_next_term(term_to_try)
                customer.loan_request.given_term = term_to_try
            else:
                customer.loan_request.result = 'approved'
                return True
        customer.loan_request.result = 'refused'
        customer.loan_request.refused_policy = 'commitment'
        return False

    def check_available_loan_term(
        self, customer: Customer, term_taxes: TermTaxes
    ):
        term_value = TermCalc(term_taxes).calc_term_value(
            customer.loan_request.amount,
            customer.loan_request.given_term
        )
        available_income = IncomeCommitment(
            customer.loan_request.commitment
        ).available_income(customer.loan_request.income)
        if term_value > available_income:
            return False
        customer.loan_request.given_amount = customer.loan_request.amount
        customer.loan_request.given_term_value = term_value
        return True
