class GenericError(Exception):
    status_code = 500

    def __init__(self, message: str, status_code : int = None, payload = None) -> None:
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code or self.status_code
        self.payload = payload

    def to_dict(self) -> dict:
        rv = dict(self.payload or {})
        rv["message"] = self.message
        return rv


class BadRequestError(GenericError):
    def __init__(self, message : str = "Bad Request", payload=None):
        GenericError.__init__(self, message, 400, payload=payload)


class UnauthorizedError(GenericError):
    def __init__(self, message : str = "Unauthorized", payload=None):
        GenericError.__init__(self, message, 401, payload=payload)


class NotFoundError(GenericError):
    def __init__(self, message : str = "Not Found", payload=None):
        GenericError.__init__(self, message, 404, payload=payload)


class UnprivilegedError(GenericError):
    def __init__(self, message : str = "Unprivileged", payload=None):
        GenericError.__init__(self, message, 400, payload=payload)

class ECGException(GenericError):
    def __init__(self, message : str = "ECG Exception", payload=None):
        GenericError.__init__(self, message, 400, payload=payload)

class CreateUserException(GenericError):
    def __init__(self, message : str = "Unable to create user", payload=None):
        GenericError.__init__(self, message, 409, payload=payload)