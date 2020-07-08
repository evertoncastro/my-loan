from datetime import date

class CustomerLoan:

    def __init__(self, amount: float, terms: int, income: float):
        self._amount = amount
        self._terms = terms
        self._income = income


class Customer:

    def __init__(
        self, cpf: str, name: str, birthdate: date, loan: CustomerLoan
    ):
        self._cpf = cpf
        self._name = name
        self._birthdate = birthdate
        self._loan = loan

    @property
    def cpf(self):
        return self._cpf

    @property
    def birthdate(self):
        return self._birthdate
