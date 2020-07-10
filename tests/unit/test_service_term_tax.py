from unittest import TestCase
from services.term_tax import ScoreTermTaxes
from services.term_tax import TermTaxes
from services.loan import TermCalc
from decimal import Decimal, ROUND_HALF_UP


class TestTermTaxes(TestCase):

    def test_if_raises_exception_for_invalid_term(self):
        term_taxes = TermTaxes(6.4, 6.6, 6.9)
        with self.assertRaises(Exception) as e:
            term_taxes.get_tax_by_term(10)
        self.assertEquals(e.exception.args[0], 'Invalid term')

    def test_if_returns_the_right_tax(self):
        term_taxes = TermTaxes(6.4, 6.6, 6.9)
        tax = term_taxes.get_tax_by_term(12)
        self.assertEquals(tax, 6.9)

    def test_if_gets_next_term_value(self):
        term_taxes = TermTaxes(6.4, 6.6, 6.9)
        next_term = term_taxes.get_next_term(6)
        self.assertEquals(next_term, 9)


class TestTaxes(TestCase):

    def test_if_returns_the_right_tax_for_699(self):
        term_taxes = ScoreTermTaxes().get_by_score(699)
        self.assertIsInstance(term_taxes, TermTaxes)
        self.assertEquals(term_taxes.get_tax_by_term(6), 6.4)
        self.assertEquals(term_taxes.get_tax_by_term(9), 6.6)
        self.assertEquals(term_taxes.get_tax_by_term(12), 6.9)

    def test_if_returns_the_right_tax_for_700(self):
        term_taxes = ScoreTermTaxes().get_by_score(700)
        self.assertIsInstance(term_taxes, TermTaxes)
        self.assertEquals(term_taxes.get_tax_by_term(6), 5.5)
        self.assertEquals(term_taxes.get_tax_by_term(9), 5.8)
        self.assertEquals(term_taxes.get_tax_by_term(12), 6.1)

    def test_if_returns_the_right_tax_for_800(self):
        term_taxes = ScoreTermTaxes().get_by_score(800)
        self.assertIsInstance(term_taxes, TermTaxes)
        self.assertEquals(term_taxes.get_tax_by_term(6), 4.7)
        self.assertEquals(term_taxes.get_tax_by_term(9), 5.0)
        self.assertEquals(term_taxes.get_tax_by_term(12), 5.3)

    def test_if_returns_the_right_tax_for_900(self):
        term_taxes = ScoreTermTaxes().get_by_score(900)
        self.assertIsInstance(term_taxes, TermTaxes)
        self.assertEquals(term_taxes.get_tax_by_term(6), 3.9)
        self.assertEquals(term_taxes.get_tax_by_term(9), 4.2)
        self.assertEquals(term_taxes.get_tax_by_term(12), 4.5)

    def test_if_raises_exception_for_invalid_score(self):
        with self.assertRaises(Exception) as e:
            ScoreTermTaxes().get_by_score(599)
        self.assertEquals(e.exception.args[0], 'Invalid score')

        with self.assertRaises(Exception) as e:
            ScoreTermTaxes().get_by_score(1001)
        self.assertEquals(e.exception.args[0], 'Invalid score')


class TestTermCalc(TestCase):

    def test_if_returns_the_correct_term_value_for_6_terms(self):
        term_value = TermCalc(
            TermTaxes(6.4, 6.6, 6.9)
        ).calc_term_value(2000, 6)
        self.assertEquals(
            term_value,
            Decimal(411.85).quantize(
                Decimal('0.00'),
                rounding=ROUND_HALF_UP
            )
        )

    def test_if_returns_the_correct_term_value_for_9_terms(self):
        term_value = TermCalc(
            TermTaxes(6.4, 6.6, 6.9)
        ).calc_term_value(2000, 9)
        self.assertEquals(
            term_value,
            Decimal(301.77).quantize(
                Decimal('0.00'),
                rounding=ROUND_HALF_UP
            )
        )

    def test_if_returns_the_correct_term_value_for_12_terms(self):
        term_value = TermCalc(
            TermTaxes(6.4, 6.6, 6.9)
        ).calc_term_value(2000, 12)
        self.assertEquals(
            term_value,
            Decimal(250.46).quantize(
                Decimal('0.00'),
                rounding=ROUND_HALF_UP
            )
        )
