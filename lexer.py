import sys
from error import *
from cstoken import *


class Lexer():
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[self.pos] if self.pos < len(
            self.text) else None
        self.in_formatted_string = False
        self.in_f_string_var = False

    def error(self):
        s = f"\u001b[31mError on '{self.current_char}' column: {self.pos}\u001b[0m"
        raise LexerError(message=s)

    def advance(self, amount=1):
        while amount > 0:
            self.pos += 1
            amount -= 1
            if self.pos > len(self.text) - 1:
                self.current_char = None
                break
            else:
                self.current_char = self.text[self.pos]
                if self.current_char == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1

    def peek(self, peek_amount=1):
        peek_pos = self.pos + peek_amount
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def check(self, string):
        end_pos = self.pos + len(string)
        if end_pos > len(self.text):
            return False
        return self.text[self.pos: end_pos].upper() == string.upper()

    def get_next_token(self):
        while True:
            if self.current_char == "`":
                self.in_formatted_string = not self.in_formatted_string
                self.advance()
                return Token(
                    TokenType.BACKTICK,
                    TokenType.BACKTICK.value,
                    self.line,
                    self.column
                )

            if self.in_formatted_string:
                if self.current_char == "{":
                    self.in_f_string_var = True
                if not self.in_f_string_var:
                    return self.f_string_portion()
                if self.current_char == "}":
                    self.in_f_string_var = False

            if self.current_char and self.current_char.isspace():
                self.advance()
                continue

            if self.current_char == '#':
                self.advance()
                while self.current_char and self.current_char != '#':
                    self.advance()
                self.advance()
                continue

            if not self.current_char:
                return Token(TokenType.EOF, None, self.line, self.column + 1)

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == "'" or self.current_char == '"':
                return self.string()

            if self.current_char.upper() == 'T' or self.current_char.upper() == 'F' and self.peek().upper() not in ('R', 'W', 'A', 'I'):
                return self.boolean()

            if self.current_char.isalpha():
                return self.id()

            if self.check('**'):
                self.advance(2)
                return Token(
                    TokenType.EXPO,
                    TokenType.EXPO.value,
                    self.line,
                    self.column
                )

            if self.check('//'):
                self.advance(2)
                return Token(
                    TokenType.INT_DIV,
                    TokenType.INT_DIV.value,
                    self.line,
                    self.column
                )

            if self.check('++'):
                self.advance(2)
                return Token(
                    TokenType.PLUS_PLUS,
                    TokenType.PLUS_PLUS.value,
                    self.line,
                    self.column
                )

            if self.check('--'):
                self.advance(2)
                return Token(
                    TokenType.MINUS_MINUS,
                    TokenType.MINUS_MINUS.value,
                    self.line,
                    self.column
                )

            if self.check('<='):
                self.advance(2)
                return Token(
                    TokenType.LTHAN_OR_EQUAL,
                    TokenType.LTHAN_OR_EQUAL.value,
                    self.line,
                    self.column
                )

            if self.check('>='):
                self.advance(2)
                return Token(
                    TokenType.GTHAN_OR_EQUAL,
                    TokenType.GTHAN_OR_EQUAL.value,
                    self.line,
                    self.column
                )

            if self.check('<\\'):
                self.advance(2)
                return Token(
                    TokenType.LTHAN,
                    TokenType.LTHAN.value,
                    self.line,
                    self.column
                )

            if self.check('>\\'):
                self.advance(2)
                return Token(
                    TokenType.GTHAN,
                    TokenType.GTHAN.value,
                    self.line,
                    self.column
                )

            if self.check('!='):
                self.advance(2)
                return Token(
                    TokenType.NOT_EQUAL,
                    TokenType.NOT_EQUAL.value,
                    self.line,
                    self.column
                )

            if self.check('=>'):
                self.advance(2)
                return Token(
                    TokenType.SET_TO,
                    TokenType.SET_TO.value,
                    self.line,
                    self.column
                )

            if self.check('??'):
                self.advance(2)
                return Token(
                    TokenType.WHILE,
                    TokenType.WHILE.value,
                    self.line,
                    self.column
                )

            if self.check('?/'):
                self.advance(2)
                return Token(
                    TokenType.FOR,
                    TokenType.FOR.value,
                    self.line,
                    self.column
                )

            if self.check('||'):
                self.advance(2)
                return Token(
                    TokenType.PARAM_SEP,
                    TokenType.PARAM_SEP.value,
                    self.line,
                    self.column
                )

            try:
                token_type = TokenType(self.current_char)
            except:
                self.error()
            else:
                token = Token(
                    type=token_type,
                    value=token_type.value,
                    line=self.line,
                    column=self.column
                )
                self.advance()
                return token

    def number(self):
        token = Token(type=None, value=None,
                      line=self.line, column=self.column)

        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.' and (peeked_char := self.peek()) and peeked_char.isdigit():
            result += self.current_char
            self.advance()

            while self.current_char and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            token.type = TokenType.FLOAT_CONST
            token.value = float(result)
        else:
            token.type = TokenType.INT_CONST
            token.value = int(result)

        return token

    def string(self):
        result = ''
        col = self.column
        line = self.line
        marker = self.current_char
        self.advance()
        while self.current_char and self.current_char != marker:
            if self.current_char == "\\":
                result += self.current_char
                self.advance()
            result += self.current_char
            self.advance()
        self.advance()

        return Token(type=TokenType.STR_CONST, value=result, line=line, column=col)

    def f_string_portion(self):
        if not self.current_char:
            return Token(TokenType.EOF, None, self.line, self.column)
        result = ''
        col = self.column
        line = self.line
        while self.current_char and self.current_char not in "`{":
            if self.current_char == "\\":
                result += self.current_char
                self.advance()
            result += self.current_char
            self.advance()

        return Token(TokenType.STR_CONST, result, line, col)

    def boolean(self):
        result = self.current_char.upper() == 'T'
        col = self.column
        line = self.line
        self.advance()
        return Token(type=TokenType.BOOL_CONST, value=result, line=line, column=col)

    def id(self):
        token = Token(type=None, value=None,
                      line=self.line, column=self.column)
        result = ''
        while self.current_char and self.current_char.isalpha():
            result += self.current_char
            self.advance()

        token_type = RESERVED_KEYWORDS.get(result.upper())
        if token_type is None:
            token.type = TokenType.FUNCTION
            token.value = result
        else:
            # reserved keyword
            token.type = token_type
            token.value = result

        return token


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Unspecified file")
    else:
        file_path = sys.argv[1]
        with open(file_path) as file:
            lexer = Lexer(file.read())
        while True:
            token = lexer.get_next_token()
            input(token)
            if token.type == TokenType.EOF:
                break
