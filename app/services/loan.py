from decimal import Decimal, ROUND_HALF_UP
from services.term_tax import TermTaxes


class IncomeCommitment:

    def __init__(self, commitment: float):
        self._commitment = commitment

    def available_income(self, income: float) -> float:
        return Decimal(income * (1 - self._commitment)).quantize(
            Decimal('0.00'),
            rounding=ROUND_HALF_UP
        )


class TermCalc:

    def __init__(self, term_taxes: TermTaxes):
        self._term_taxes = term_taxes

    def calc_term_value(self, current_value: float, term: int) -> float:
        # TODO: Seria adequado utilizar uma convensao para valores monetarios
        i = self._term_taxes.get_tax_by_term(term) / 100
        n = term
        final = current_value * ((((1 + i)**n) * i) / (((1 + i)**n) - 1))
        return Decimal(final).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)