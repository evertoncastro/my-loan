from unittest import TestCase
from mock import patch
from services.policies import AgePolicy
from services.policies import ScorePolicy
from services.policies import IncomeCommitmentPolicy
from entities import Customer
from entities import LoanRequest
from util import date
from datetime import datetime
from tests.fixtures.stubs import FakeResponse
from services.term_tax import ScoreTermTaxes


class TestAgePolicy(TestCase):

    @patch('services.policies.date.current_datetime')
    def test_if_return_false_for_less_than_18(self, mock_dtime):
        mock_dtime.return_value = datetime(2018, 10, 10)
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-07-06'),
            LoanRequest(500, 6, 1000)
        )
        policy_result = AgePolicy().execute(customer)
        self.assertFalse(policy_result)
        self.assertEquals(customer.loan_request.result, 'refused')
        self.assertEquals(customer.loan_request.refused_policy, 'age')

    @patch('services.policies.date.current_datetime')
    def test_if_return_true_for_exactly_18(self, mock_dtime):
        mock_dtime.return_value = datetime(2020, 1, 1)
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            LoanRequest(500, 6, 1000)
        )
        policy_result = AgePolicy().execute(customer)
        self.assertTrue(policy_result)


class TestScorePolicy(TestCase):

    def setUp(self):
        self.customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            LoanRequest(500, 6, 1000)
        )

    @patch('services.policies.post')
    def test_if_calls_post_with_rigth_params(self, mock_post):
        mock_post.return_value = FakeResponse(200, {'score': 800})
        ScorePolicy().execute(self.customer)
        mock_post.assert_called_with(
            'https://challenge.noverde.name/score',
            data='{"cpf": "11122233344"}',
            headers={'x-api-key': 'SnAB7jQEFs1Ai8XtZdssa14gORT3jWPI7TWdXN97'}
        )

    @patch('services.policies.post')
    def test_if_returns_false_for_lower_score(self, mock_post):
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            LoanRequest(500, 6, 1000)
        )
        mock_post.return_value = FakeResponse(200, {'score': 599})
        policy_response = ScorePolicy().execute(customer)
        self.assertFalse(policy_response)
        self.assertEquals(customer.loan_request.result, 'refused')
        self.assertEquals(customer.loan_request.refused_policy, 'score')

    @patch('services.policies.post')
    def test_if_returns_true_for_minimun_score(self, mock_post):
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            LoanRequest(500, 6, 1000)
        )
        mock_post.return_value = FakeResponse(200, {'score': 600})
        policy_response = ScorePolicy().execute(customer)
        self.assertTrue(policy_response)
        self.assertEquals(customer.loan_request.score, 600)


class TestIncomeCommitmentPolicy(TestCase):

    def setUp(self):
        self.customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            LoanRequest(500, 6, 1000)
        )

    @patch('services.policies.post')
    def test_if_calls_post_with_rigth_params(self, mock_post):
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            LoanRequest(500, 6, 1000)
        )
        customer.loan_request.score = 750
        mock_post.return_value = FakeResponse(200, {'commitment': 0.85})
        IncomeCommitmentPolicy().execute(customer)
        mock_post.assert_called_with(
            'https://challenge.noverde.name/commitment',
            data='{"cpf": "11122233344"}',
            headers={'x-api-key': 'SnAB7jQEFs1Ai8XtZdssa14gORT3jWPI7TWdXN97'}
        )

    @patch('services.policies.post')
    def test_if_updates_customer_request_commitment(self, mock_post):
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            LoanRequest(500, 6, 1000)
        )
        customer.loan_request.score = 750
        mock_post.return_value = FakeResponse(200, {'commitment': 0.85})
        IncomeCommitmentPolicy().execute(customer)
        self.assertEquals(customer.loan_request.commitment, 0.85)

    def test_if_returns_false_for_invalid_term_quantity(self):
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            LoanRequest(2500, 9, 1000)
        )
        customer.loan_request.score = 750
        customer.loan_request.commitment = 0.7
        term_taxes = ScoreTermTaxes().get_by_score(
            customer.loan_request.score
        )

        valid = IncomeCommitmentPolicy().check_available_loan_term(
            customer, term_taxes)
        self.assertFalse(valid)

    def test_if_returns_true_for_invalid_term_quantity(self):
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            LoanRequest(2500, 12, 1000)
        )
        customer.loan_request.score = 750
        customer.loan_request.commitment = 0.7
        term_taxes = ScoreTermTaxes().get_by_score(
            customer.loan_request.score
        )

        valid = IncomeCommitmentPolicy().check_available_loan_term(
            customer, term_taxes)
        self.assertTrue(valid)

    def test_if_returns_false_for_invalid_loan(self):
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            LoanRequest(2500, 6, 800)
        )
        customer.loan_request.score = 750
        customer.loan_request.commitment = 0.7

        valid = IncomeCommitmentPolicy().check_given_loan(customer)
        self.assertFalse(valid)
        self.assertEquals(customer.loan_request.result, 'refused')
        self.assertEquals(customer.loan_request.refused_policy, 'commitment')

    def test_if_returns_true_for_valid_loan(self):
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            LoanRequest(2500, 6, 1500)
        )
        customer.loan_request.score = 750
        customer.loan_request.commitment = 0.7

        valid = IncomeCommitmentPolicy().check_given_loan(customer)
        self.assertTrue(valid)
        self.assertEquals(customer.loan_request.result, 'approved')
        self.assertEquals(customer.loan_request.given_amount, 2500)
        self.assertEquals(customer.loan_request.given_term, 9)

    @patch('services.policies.post')
    def test_if_returns_false_for_refused_income_policy(self, mock_post):
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            LoanRequest(3000, 6, 1000)
        )
        customer.loan_request.score = 750

        mock_post.return_value = FakeResponse(200, {'commitment': 0.7})
        policy_response = IncomeCommitmentPolicy().execute(customer)

        self.assertFalse(policy_response)
        self.assertEquals(customer.loan_request.result, 'refused')
        self.assertEquals(customer.loan_request.refused_policy, 'commitment')

    @patch('services.policies.post')
    def test_if_returns_true_for_refused_income_policy(self, mock_post):
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            LoanRequest(3000, 6, 2000)
        )
        customer.loan_request.score = 750

        mock_post.return_value = FakeResponse(200, {'commitment': 0.7})
        policy_response = IncomeCommitmentPolicy().execute(customer)

        self.assertTrue(policy_response)
        self.assertEquals(customer.loan_request.result, 'approved')
        self.assertEquals(customer.loan_request.refused_policy, None)