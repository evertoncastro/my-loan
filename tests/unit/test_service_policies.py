from unittest import TestCase
from mock import patch
from services.policies import AgePolicy
from services.customer import Customer
from services.customer import CustomerLoan
from util import date
from datetime import datetime


class TestAgePolicy(TestCase):

    @patch('services.policies.date.current_datetime')
    def test_if_return_false_for_less_than_18(self, mock_dtime):
        mock_dtime.return_value = datetime(2018, 10, 10)
        customer = Customer(
            '11122233344',
            'Chris',
            date.iso_date_to_datetime('2002-07-06'),
            CustomerLoan(
                500, 6, 1000
            )
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
            CustomerLoan(
                500, 6, 1000
            )
        )
        policy_result = AgePolicy().execute(customer)
        self.assertTrue(policy_result)
