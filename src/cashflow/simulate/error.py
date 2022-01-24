"""This provides a base class for errors."""


class InputConfigurationError(BaseException):
    def __init__(self, message: str):
        msg_header = "*" * 79
        msg_header += "\n[Input Configuration Error]:\n\n"
        super().__init__(message)
