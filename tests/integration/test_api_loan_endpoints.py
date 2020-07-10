from unittest import TestCase
from main import app
from app import db
from tests.runner import clear_database
from models import LoanRequestModel


class TestEpisodeNamespace(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.db = db
        self.session = self.db.session

        clear_database(self.db)

    def tearDown(self):
        clear_database(self.db)

    def test_if_returns_badrequest_for_empty_params(self):
        response = self.client.post(
            '/loan_api/v1.0/loan/',
            json={}
        )
        self.assertEqual(response.status_code, 400)

    def test_if_returns_badrequest_for_invalid_cpf(self):
        response = self.client.post(
            '/loan_api/v1.0/loan/',
            json={
                    "name": "string",
                    "cpf": "90971077091",
                    "birthdate": "1989-09-02",
                    "amount": 1000,
                    "terms": 6,
                    "income": 0
                }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'errors': ['Invalid cpf']})

    def test_if_returns_200_for_valid_payload(self):
        response = self.client.post(
            '/loan_api/v1.0/loan/',
            json={
                    "name": "string",
                    "cpf": "90971077096",
                    "birthdate": "1989-09-02",
                    "amount": 1000,
                    "terms": 6,
                    "income": 0
                }
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json['id'])

        loan_data = LoanRequestModel().fetch(
            self.session, response.json['id']
        )
        self.assertIsNotNone(loan_data)
