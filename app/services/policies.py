from abc import ABC
from abc import abstractmethod
from services.customer import Customer
from util import date
from dateutil.relativedelta import relativedelta


class Policy(ABC):

    @abstractmethod
    def execute(self, customer: Customer) -> bool:
        pass


class AgePolicy(Policy):

    def execute(self, customer):
        current_date = date.current_datetime()
        date_diff = relativedelta(current_date, customer.birthdate)
        if date_diff.years < 18:
            return False
        return True
