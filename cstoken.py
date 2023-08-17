from enum import Enum


class TokenType(Enum):
    MEMORY = 'M'
    SET = 'S'  # Set Var
    RETURN = 'R'
    BREAK = 'B'
    CONTINUE = 'C'
    FILE_READ = 'FR'
    FILE_WRITE = 'FW'
    FILE_APPEND = 'FA'
    NULL = 'X'
    IF = '?'
    ELSE = 'E'
    WHILE = '??'
    FOR = '?/'
    PYTHON = '^'
    IMPORT = '@'
    MODULE = '$'
    LCURLY = '{'
    RCURLY = '}'
    LBRACKET = '['
    RBRACKET = ']'
    LPAREN = '('
    RPAREN = ')'
    LANGLE = '<'
    RANGLE = '>'
    PARAM_SEP = '||'
    SET_TO = '=>'
    LTHAN = '</'
    GTHAN = '>/'
    LTHAN_OR_EQUAL = '<='
    GTHAN_OR_EQUAL = '>='
    EQUAL = '='
    NOT_EQUAL = '!='
    NOT = '!'
    AND = '&'
    OR = '|'
    COLON = ':'
    SEMI = ';'
    PERIOD = '.'
    COMMA = ','
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    EXPO = '**'
    INT_DIV = '//'
    FLOAT_DIV = '/'
    MOD = "%"
    PLUS_PLUS = '++'
    MINUS_MINUS = '--'
    INT_CONST = 'INT_CONST'
    FLOAT_CONST = 'FLOAT_CONST'
    STR_CONST = 'STR_CONST'
    BOOL_CONST = 'BOOL_CONST'
    FUNCTION = 'FUNCTION'
    EOF = 'EOF'


def _build_reserved_keywords():
    tt_list = list(TokenType)
    start_index = tt_list.index(TokenType.MEMORY)
    end_index = tt_list.index(TokenType.ELSE)
    reserved_keywords = {
        token_type.value: token_type
        for token_type in tt_list[start_index:end_index + 1]
    }
    return reserved_keywords


RESERVED_KEYWORDS = _build_reserved_keywords()


class Token():
    def __init__(self, type, value, line=None, column=None):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()
