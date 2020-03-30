class Response:

    def __init__(self, data, message):
        self.message = message
        self.data = data


class Success(Response):

    def __init__(self, data, message):
        super().__init__(data, message)
        self.color = "success"


class Error(Response):

    def __init__(self, data, message):
        super().__init__(data, message)
        self.color = "danger"
