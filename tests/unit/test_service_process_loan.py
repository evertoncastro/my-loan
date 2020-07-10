from main import app
from app import db
from mock import patch
from unittest import TestCase
from tests.runner import clear_database
from services.process_loan import async_process_loan_registry
from services.process_loan import process_loan_policies
from services.process_loan import update_loan_registry
from models import LoanRequestModel
from datetime import datetime
from entities import Customer
from entities import LoanRequest


class TestAsyncProcessLoan(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.db = db
        self.session = self.db.session
        clear_database(self.db)

    def tearDown(self):
        clear_database(self.db)

    def test_if_returns_false_for_not_found_registry(self):
        processed = async_process_loan_registry('xpto')
        self.assertFalse(processed)

    @patch('services.process_loan.process_loan_policies')
    def test_if_process_loan_registry(
        self,
        mock_proc_policies
    ):
        loan_registry = LoanRequestModel().create(
            self.session,
            id='xpto',
            cpf='00011122233',
            name='Fake',
            birthdate=datetime.strptime('1990-01-01', '%Y-%m-%d'),
            amount=2000,
            terms=6,
            income=3000
        )
        self.session.commit()
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
        mock_proc_policies.return_value = customer
        processed = async_process_loan_registry('xpto')
        self.assertTrue(processed)
        self.assertEqual(loan_registry.status, 'completed')


class TestProcessLoanPolicies(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.db = db
        self.session = self.db.session
        clear_database(self.db)

    def tearDown(self):
        clear_database(self.db)

    @patch('services.process_loan.AgePolicy.execute')
    def test_if_calls_age_policy(self, mock_age_execute):
        mock_age_execute.return_value = False
        loan_registry = LoanRequestModel().create(
            self.session,
            id='xpto',
            cpf='00011122233',
            name='Fake',
            birthdate=datetime.strptime('1990-01-01', '%Y-%m-%d'),
            amount=2000,
            terms=6,
            income=3000
        )
        self.session.commit()
        process_loan_policies(loan_registry)
        mock_age_execute.assert_called()

    @patch('services.process_loan.ScorePolicy.execute')
    @patch('services.process_loan.AgePolicy.execute')
    def test_if_calls_score_policy(
        self,
        mock_age_execute,
        mock_score_policy
    ):
        mock_age_execute.return_value = True
        mock_score_policy.return_value = False
        loan_registry = LoanRequestModel().create(
            self.session,
            id='xpto',
            cpf='00011122233',
            name='Fake',
            birthdate=datetime.strptime('1990-01-01', '%Y-%m-%d'),
            amount=2000,
            terms=6,
            income=3000
        )
        self.session.commit()
        process_loan_policies(loan_registry)
        mock_score_policy.assert_called()

    @patch('services.process_loan.IncomeCommitmentPolicy.execute')
    @patch('services.process_loan.ScorePolicy.execute')
    @patch('services.process_loan.AgePolicy.execute')
    def test_if_calls_commitment_policy(
        self,
        mock_age_execute,
        mock_score_policy,
        mock_commitment_policy
    ):
        mock_age_execute.return_value = True
        mock_score_policy.return_value = True

        loan_registry = LoanRequestModel().create(
            self.session,
            id='xpto',
            cpf='00011122233',
            name='Fake',
            birthdate=datetime.strptime('1990-01-01', '%Y-%m-%d'),
            amount=2000,
            terms=6,
            income=3000
        )
        self.session.commit()
        process_loan_policies(loan_registry)
        mock_commitment_policy.assert_called()


class TestUpdateLoanRegistry(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.db = db
        self.session = self.db.session
        clear_database(self.db)

    def tearDown(self):
        clear_database(self.db)

    def test_if_updates_with_completed_approved_process(self):
        loan_registry = LoanRequestModel().create(
            self.session,
            id='xpto',
            cpf='00011122233',
            name='Fake',
            birthdate=datetime.strptime('1990-01-01', '%Y-%m-%d'),
            amount=2000,
            terms=6,
            income=3000
        )
        self.session.commit()
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
        customer.loan_request.result = 'approved'
        customer.loan_request.given_amount = 2000
        customer.loan_request.given_term = 9

        update_loan_registry(loan_registry, customer)

        self.assertEqual(loan_registry.result, 'approved')
        self.assertEqual(loan_registry.approved_amount, 2000)
        self.assertEqual(loan_registry.approved_terms, 9)
        self.assertEqual(loan_registry.status, 'completed')

    def test_if_updates_with_completed_refused_process(self):
        loan_registry = LoanRequestModel().create(
            self.session,
            id='xpto',
            cpf='00011122233',
            name='Fake',
            birthdate=datetime.strptime('1990-01-01', '%Y-%m-%d'),
            amount=2000,
            terms=6,
            income=3000
        )
        self.session.commit()
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
        customer.loan_request.result = 'refused'
        customer.loan_request.refused_policy = 'score'

        update_loan_registry(loan_registry, customer)

        self.assertEqual(loan_registry.result, 'refused')
        self.assertEqual(loan_registry.refused_policy, 'score')