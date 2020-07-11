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
    print('Start async process')
    print(f'ID: {_id}')
    try:
        session = db.session
        loan_registry = LoanRequestModel().fetch(
            session, _id
        )
        if not loan_registry:
            print('Not found loan registry')
            return False
        print('Rigistry found')
        customer = process_loan_policies(loan_registry)
        update_loan_registry(loan_registry, customer)
        session.commit()
        return True
    except Exception as e:
        print(f'Error: {e.args}')
        raise e
    finally:
        session.close()


def process_loan_policies(loan_registry: LoanRequestModel) -> Customer:
    print('start processing policies')
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


def update_loan_registry(
    loan_registry: LoanRequestModel,
    customer: Customer
):
    print('Start updated registry')
    if customer.loan_request.result == 'approved':
        loan_registry.result = 'approved'
        loan_registry.approved_amount = customer.loan_request.amount
        loan_registry.approved_terms = customer.loan_request.given_term
    elif customer.loan_request.result == 'refused':
        loan_registry.result = 'refused'
        loan_registry.refused_policy = customer.loan_request.refused_policy
    loan_registry.status = 'completed'
