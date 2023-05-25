from enum import Enum


class ErrorCode(Enum):
    UNEXPECTED_TOKEN = 'Unexpected token'
    ID_NOT_FOUND = 'Identifier not found'
    WRONG_PARAMS_NUM = 'Wrong number of parameters'
    FILE_NOT_FOUND = 'File not found'
    MODULE_NOT_FOUND = 'Module not found'
    CIRCULAR_IMPORT = 'Circular import'


class Error(Exception):
    def __init__(self, error_code=None, token=None, message=None):
        self.error_code = error_code
        self.token = token
        self.message = message
        super().__init__(message)


class LexerError(Error):
    pass


class ParserError(Error):
    pass


class SemanticError(Error):
    pass


class InterpreterError(Error):
    pass
