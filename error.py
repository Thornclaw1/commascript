from enum import Enum


class ErrorCode(Enum):
    UNEXPECTED_TOKEN = 'Unexpected token'
    ID_NOT_FOUND = 'Identifier not found'
    WRONG_PARAMS_NUM = 'Wrong number of parameters'
    PARAMETER_ERROR = 'Parameter error'
    INVALID_RETURN_STATEMENT = 'Invalid Return Statement'
    FILE_NOT_FOUND = 'File not found'
    MODULE_NOT_FOUND = 'Module not found'
    CIRCULAR_IMPORT = 'Circular import'
    INVALID_INDEXER = 'Invalid use of an indexer'
    INDEX_ERROR = 'Index out of range'
    KEY_NOT_FOUND = 'Key not found'
    VALUE_NOT_FOUND = 'Value not found'
    VARIABLE_MISSING = 'A variable seems to be missing'
    TYPE_ERROR = 'Type error'
    INVALID_FUNCTION_CALL = 'Invalid Function Call'


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
