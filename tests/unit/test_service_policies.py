from unittest import TestCase
from mock import patch
from services.policies import AgePolicy
from services.policies import ScorePolicy
from services.policies import IncomeCommitmentPolicy
from services.customer import Customer
from services.customer import CustomerLoan
from util import date
from datetime import datetime
from ..fixtures.stubs import FakeResponse


class TestAgePolicy(TestCase):

    @patch('services.policies.date.current_datetime')
    def test_if_return_false_for_less_than_18(self, mock_dtime):
        mock_dtime.return_value = datetime(2018, 10, 10)
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-07-06'),
            CustomerLoan(500, 6, 1000)
        )
        policy_result = AgePolicy().execute(customer)
        self.assertFalse(policy_result)

    @patch('services.policies.date.current_datetime')
    def test_if_return_true_for_exactly_18(self, mock_dtime):
        mock_dtime.return_value = datetime(2020, 1, 1)
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            CustomerLoan(500, 6, 1000)
        )
        policy_result = AgePolicy().execute(customer)
        self.assertTrue(policy_result)


class TestScorePolicy(TestCase):

    def setUp(self):
        self.customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            CustomerLoan(500, 6, 1000)
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
        mock_post.return_value = FakeResponse(200, {'score': 599})
        policy_response = ScorePolicy().execute(self.customer)
        self.assertFalse(policy_response)

    @patch('services.policies.post')
    def test_if_returns_true_for_minimun_score(self, mock_post):
        mock_post.return_value = FakeResponse(200, {'score': 600})
        policy_response = ScorePolicy().execute(self.customer)
        self.assertTrue(policy_response)


class TestIncomeCommitmentPolicy(TestCase):

    def setUp(self):
        self.customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-01-01'),
            CustomerLoan(500, 6, 1000)
        )

    @patch('services.policies.post')
    def test_if_calls_post_with_rigth_params(self, mock_post):
        mock_post.return_value = FakeResponse(200, {'commitment': 0.85})
        IncomeCommitmentPolicy().execute(self.customer)
        mock_post.assert_called_with(
            'https://challenge.noverde.name/commitment',
            data='{"cpf": "11122233344"}',
            headers={'x-api-key': 'SnAB7jQEFs1Ai8XtZdssa14gORT3jWPI7TWdXN97'}
        )

    # @patch('services.policies.post')
    # def test_if_returns_false_not_enougth_income(self, mock_post):
    #     mock_post.return_value = FakeResponse(200, {'commitment': 599})
    #     policy_response = ScorePolicy().execute(self.customer)
    #     self.assertFalse(policy_response)