from enum import Enum

class TokenType(Enum):
    MEMORY = 'M' # Memory
    SET = 'S' # Set Var
    RETURN = 'R' # Return
    INPUT = 'I' # Input
    PRINT = 'P' # Print
    RANDOM_INT = 'RND'
    CAST_STR = 'CS'
    CAST_INT = 'CI'
    CAST_FLOAT = 'CF'
    CAST_BOOL = 'CB'
    IF = '?'
    ELSE = 'E'
    WHILE = '??'
    # LCURLY = '{'
    # RCURLY = '}'
    LPAREN = '('
    RPAREN = ')'
    LANGLE = '<'
    RANGLE = '>'
    SET_TO = '=>'
    LTHAN = '=-'
    GTHAN = '=+'
    LTHAN_OR_EQUAL = '=-='
    GTHAN_OR_EQUAL = '=+='
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
    INT_DIV = '//'
    FLOAT_DIV = '/'
    MOD = "%"
    INT_CONST = 'INT_CONST'
    FLOAT_CONST = 'FLOAT_CONST'
    STR_CONST = 'STR_CONST'
    EOF = 'EOF'

# def _build_reserved_keywords():
#     tt_list = list(TokenType)
#     start_index = tt_list.index(TokenType.M)
#     end_index = tt_list.index(TokenType.P)
#     reserved_keywords = {
#         token_type.value: token_type
#         for token_type in tt_list[start_index:end_index + 1]
#     }
#     return reserved_keywords

# RESERVED_KEYWORDS = _build_reserved_keywords()
# RESERVED_KEYWORDS = {}

class Token():
    def __init__(self, type, value, column=None):
        self.type = type
        self.value = value
        self.column = column
    
    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()