class Response:

    def __init__(self, callback, logs, message):
        self.message = message
        self.callback = callback
        self.logs = logs


class Success(Response):

    def __init__(self, callback, logs, message):
        super().__init__(callback, logs, message)
        self.color = "success"
        self.code = 200


class Error(Response):

    def __init__(self, callback, logs, message):
        super().__init__(callback, logs, message)
        self.color = "danger"
        self.code = 400
