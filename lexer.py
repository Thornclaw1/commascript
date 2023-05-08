import sys
from error import *
from cstoken import *

class Lexer():
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        
    def error(self):
        s = f"Error on '{self.current_char}' column: {self.pos}"
        raise LexerError(message=s)

    def advance(self, amount = 1):
        self.pos += amount
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self, peek_amount = 1):
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
            while self.current_char and self.current_char.isspace():
                self.advance()

            if self.current_char == '#':
                self.advance()
                while self.current_char and self.current_char != '#':
                    self.advance()
                self.advance()
                continue

            if not self.current_char:
                return Token(TokenType.EOF, None)
                
            if self.current_char.isdigit():
                return self.number()
            
            if self.current_char == "'" or self.current_char == '"':
                return self.string()

            if self.current_char.upper() == 'T' or self.current_char.upper() == 'F':
                return self.boolean()

            # if self.current_char.isalpha():
            #     return self.id()

            if self.check('**'):
                self.advance(2)
                return Token(
                    TokenType.EXPO,
                    TokenType.EXPO.value
                )
            
            if self.check('//'):
                self.advance(2)
                return Token(
                    TokenType.INT_DIV, 
                    TokenType.INT_DIV.value
                )
            
            if self.check('=-='):
                self.advance(3)
                return Token(
                    TokenType.LTHAN_OR_EQUAL,
                    TokenType.LTHAN_OR_EQUAL.value
                )
            
            if self.check('=+='):
                self.advance(3)
                return Token(
                    TokenType.GTHAN_OR_EQUAL,
                    TokenType.GTHAN_OR_EQUAL.value
                )
            
            if self.check('=-'):
                self.advance(2)
                return Token(
                    TokenType.LTHAN,
                    TokenType.LTHAN.value
                )
            
            if self.check('=+'):
                self.advance(2)
                return Token(
                    TokenType.GTHAN,
                    TokenType.GTHAN.value
                )
            
            if self.check('!='):
                self.advance(2)
                return Token(
                    TokenType.NOT_EQUAL,
                    TokenType.NOT_EQUAL.value
                )
            
            if self.check('=>'):
                self.advance(2)
                return Token(
                    TokenType.SET_TO,
                    TokenType.SET_TO.value
                )
            
            if self.check('??'):
                self.advance(2)
                return Token(
                    TokenType.WHILE,
                    TokenType.WHILE.value
                )

            if self.check('RND'):
                self.advance(3)
                return Token(
                    TokenType.RANDOM_INT,
                    TokenType.RANDOM_INT.value
                )

            if self.check('CS'):
                self.advance(2)
                return Token(
                    TokenType.CAST_STR,
                    TokenType.CAST_STR.value
                )

            if self.check('CI'):
                self.advance(2)
                return Token(
                    TokenType.CAST_INT,
                    TokenType.CAST_INT.value
                )

            if self.check('CF'):
                self.advance(2)
                return Token(
                    TokenType.CAST_FLOAT,
                    TokenType.CAST_FLOAT.value
                )

            if self.check('CB'):
                self.advance(2)
                return Token(
                    TokenType.CAST_BOOL,
                    TokenType.CAST_BOOL.value
                )
            
            try:
                token_type = TokenType(self.current_char.upper())
            except ValueError:
                self.error()
            else:
                token = Token(
                    type=token_type,
                    value=token_type.value,
                    column=self.pos
                )
                self.advance()
                return token

    def number(self):
        token = Token(type=None, value=None, column=self.pos)

        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
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
        col = self.pos
        marker = self.current_char
        self.advance()
        while self.current_char and self.current_char != marker:
            result += self.current_char
            self.advance()
        self.advance()

        return Token(type=TokenType.STR_CONST, value=result, column=col)

    def boolean(self):
        result = self.current_char.upper() == 'T'
        col = self.pos
        self.advance()
        return Token(type=TokenType.BOOL_CONST, value=result, column=col)

    # def id(self):
    #     token = Token(type=None, value=None, column=self.pos)

    #     result = ''
    #     while self.current_char and self.current_char.isalnum():
    #         result += self.current_char
    #         self.advance()

    #     token_type = RESERVED_KEYWORDS.get(result.upper())
    #     if token_type is None:
    #         token.type = TokenType.ID
    #         token.value = result
    #     else:
    #         # reserved keyword
    #         token.type = token_type
    #         token.value = result.upper()

    #     return token



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
            if token.type == TokenType.EOF: break