from unittest import TestCase
from services.loan import IncomeCommitment


class TestIncomeCommitment(TestCase):

    def test_if_returns_the_right_commitment_for_0_dot_8(self):
        available = IncomeCommitment(0.8).available_income(2000)
        self.assertEquals(available, 400.00)

    def test_if_returns_the_right_commitment_for_0_dot_5(self):
        available = IncomeCommitment(0.5).available_income(2000)
        self.assertEquals(available, 1000.00)
