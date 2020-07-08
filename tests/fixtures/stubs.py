from json import dumps
from json import loads


class FakeResponse:

    def __init__(self, status_code: int, payload: dict):
        self.status_code = status_code
        self.text = dumps(payload)

    def json(self):
        return loads(self.text)