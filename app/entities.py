from datetime import date


class LoanRequest:

    def __init__(self, amount: float, term: int, income: float):
        self._amount = amount
        self._term = term
        self._income = income
        self._given_term = term
        self._score = None
        self._commitment = None
        self._given_amount = None
        self._given_term_value = None
        self._result = None
        self._refused_policy = None

    def __repr__(self):
        return f'Amount {self._amount}\n' \
            f'Term {self._term}\n' \
            f'Income {self._income}\n' \
            f'Given Term {self._given_term}\n' \
            f'Score {self._score}\n' \
            f'Comitment {self._commitment}\n' \
            f'Given Amount {self._given_amount}\n' \
            f'Given Term Value {self._given_term_value}\n' \
            f'Result {self._result}\n' \
            f'Refused Policy {self._refused_policy}\n' \

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, a):
        self._amount = a

    @property
    def term(self):
        return self._term

    @term.setter
    def term(self, t):
        self._term = t

    @property
    def income(self):
        return self._income

    @income.setter
    def income(self, i):
        self._income = i

    @property
    def given_term(self):
        return self._given_term

    @given_term.setter
    def given_term(self, t):
        self._given_term = t

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, s):
        self._score = s

    @property
    def commitment(self):
        return self._commitment

    @commitment.setter
    def commitment(self, c):
        self._commitment = c

    @property
    def given_amount(self):
        return self._given_amount

    @given_amount.setter
    def given_amount(self, a):
        self._given_amount = a

    @property
    def given_term_value(self):
        return self._given_term_value

    @given_term_value.setter
    def given_term_value(self, v):
        self._given_term_value = v

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, r):
        self._result = r

    @property
    def refused_policy(self):
        return self._refused_policy

    @refused_policy.setter
    def refused_policy(self, r):
        self._refused_policy = r


class Customer:

    def __init__(
        self, cpf: str, name: str, birthdate: date, loan_req: LoanRequest
    ):
        self._cpf = cpf
        self._name = name
        self._birthdate = birthdate
        self._loan_request = loan_req

    @property
    def cpf(self):
        return self._cpf

    @property
    def birthdate(self):
        return self._birthdate

    @property
    def loan_request(self):
        return self._loan_request
