

class InvalidTermQuantity(Exception):

    def __init__(self):
        self.message = self.__class__.__name__
        super().__init__()