




class FieldExceptionValueError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)



class NullableExceptionError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)



class FieldExceptionContainsError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)