import logging
from app import db
from app import celery
from entities import Customer
from entities import LoanRequest
from models import LoanRequestModel
from services.policies import AgePolicy
from services.policies import ScorePolicy
from services.policies import IncomeCommitmentPolicy


@celery.task()
def async_process_loan_registry(_id: str) -> bool:
    logging.info('Start async process')
    logging.info(f'ID: {_id}')
    try:
        session = db.session
        loan_registry = LoanRequestModel().fetch(
            session, _id
        )
        if not loan_registry:
            logging.info('Not found loan registry')
            return False
        logging.info('Rigistry found')
        customer = process_loan_policies(loan_registry)
        update_loan_registry(loan_registry, customer)
        logging.info(customer.loan_request)
        session.commit()
        return True
    except Exception as e:
        logging.info(f'Error: {e.args}')
        raise e
    finally:
        session.close()


def process_loan_policies(loan_registry: LoanRequestModel) -> Customer:
    logging.info('start processing policies')
    customer = Customer(
        loan_registry.cpf,
        loan_registry.name,
        loan_registry.birthdate,
        LoanRequest(
            loan_registry.amount,
            loan_registry.terms,
            loan_registry.income
        )
    )
    valid = AgePolicy().execute(customer)
    if not valid:
        return customer
    valid = ScorePolicy().execute(customer)
    if not valid:
        return customer
    IncomeCommitmentPolicy().execute(customer)
    return customer


def update_loan_registry(loan_registry: LoanRequestModel, customer: Customer):
    logging.info('Start updated registry')
    if customer.loan_request.result == 'approved':
        loan_registry.result = 'approved'
        loan_registry.approved_amount = customer.loan_request.amount
        loan_registry.approved_terms = customer.loan_request.given_term
    elif customer.loan_request.result == 'refused':
        loan_registry.result = 'refused'
        loan_registry.refused_policy = customer.loan_request.refused_policy
    loan_registry.status = 'completed'
