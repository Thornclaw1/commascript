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

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def get_next_token(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

        if not self.current_char:
            return Token(TokenType.EOF, None)
            
        if self.current_char.isdigit():
            return self.number()
        
        if self.current_char == "'" or self.current_char == '"':
            return self.string()

        # if self.current_char.isalpha():
        #     return self.id()
        
        if self.current_char == '/' and self.peek() == '/':
            self.advance()
            self.advance()
            return Token(
                TokenType.INT_DIV, 
                TokenType.INT_DIV.value
            )
        
        if self.current_char == '<' and self.peek() == '<':
            self.advance()
            self.advance()
            return Token(
                TokenType.LTHAN,
                TokenType.LTHAN.value
            )
        
        if self.current_char == '>' and self.peek() == '>':
            self.advance()
            self.advance()
            return Token(
                TokenType.GTHAN,
                TokenType.GTHAN.value
            )
        
        if self.current_char == '<' and self.peek() == '=':
            self.advance()
            self.advance()
            return Token(
                TokenType.LTHAN_OR_EQUAL,
                TokenType.LTHAN_OR_EQUAL.value
            )
        
        if self.current_char == '>' and self.peek() == '=':
            self.advance()
            self.advance()
            return Token(
                TokenType.GTHAN_OR_EQUAL,
                TokenType.GTHAN_OR_EQUAL.value
            )
        
        if self.current_char == '!' and self.peek() == '=':
            self.advance()
            self.advance()
            return Token(
                TokenType.NOT_EQUAL,
                TokenType.NOT_EQUAL.value
            )
        
        if self.current_char == '=' and self.peek() == '>':
            self.advance()
            self.advance()
            return Token(
                TokenType.SET,
                TokenType.SET.value
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