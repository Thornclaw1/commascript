import sys
import ast
import inspect

from error import *
from cstoken import *
from lexer import *
from built_in_functions import *

current_print_indent = 0


class AST(object):
    pass


class Program(AST):
    def __init__(self, statement_list_node):
        self.statement_list_node = statement_list_node

    def __str__(self):
        return self.statement_list_node.__str__()


class StatementList(AST):
    def __init__(self):
        self.children = []

    def __str__(self):
        global current_print_indent
        current_print_indent += 2
        rep_str = "StatementList(\n"
        for child in self.children:
            rep_str += f"{' '*current_print_indent}{child},\n"
        current_print_indent -= 2
        rep_str += f"{' '*current_print_indent})"
        return rep_str
    __repr__ = __str__


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return f"BinOp({self.left} {self.op.value} {self.right})"
    __repr__ = __str__


class Const(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return f"{self.token.type.value}({self.value})"
    __repr__ = __str__


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def __str__(self):
        return f"UnaryOp({self.op.value} {self.expr})"
    __repr__ = __str__


class VarDecl(AST):
    def __init__(self, params_num, value):
        self.params_num = params_num
        self.value = value

    def __str__(self):
        return f"VarDecl({self.params_num}, {self.value})"
    __repr__ = __str__


class VarSet(AST):
    def __init__(self, scope_depth, mem_loc, value):
        self.scope_depth = scope_depth
        self.mem_loc = mem_loc
        self.value = value

    def __str__(self):
        return f"VarSet(s{'.'*self.scope_depth}{self.mem_loc}, {self.value})"


class VarGet(AST):
    def __init__(self, scope_depth, mem_loc, args):
        self.scope_depth = scope_depth
        self.mem_loc = mem_loc
        self.args = args

    def __str__(self):
        return f"VarGet(m{'.'*self.scope_depth}{self.mem_loc}, {self.args})"
    __repr__ = __str__


class Not(AST):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Not({self.value})"


class If(AST):
    def __init__(self, conditional, value, else_value):
        self.conditional = conditional
        self.value = value
        self.else_value = else_value

    def __str__(self):
        return f"If({self.conditional}, {self.value}, {self.else_value})"
    __repr__ = __str__


class While(AST):
    def __init__(self, conditional, value):
        self.conditional = conditional
        self.value = value

    def __str__(self):
        return f"While({self.conditional}, {self.value})"
    __repr__ = __str__


class Return(AST):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"Return({self.expr})"
    __repr__ = __str__


class BuiltInFunction(AST):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return f"BuiltInFunction({self.name}, {self.args}"
    __repr__ = __str__


class Parser():
    def __init__(self, lexer, display_debug_messages=False):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.peeked_at_token = None
        self.display_debug_messages = display_debug_messages

    def error(self, error_code, token):
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}'
        )

    def log(self, msg):
        if self.display_debug_messages:
            print(msg)

    def eat(self, token_type):
        self.log(f"Eating {self.current_token.type} as {token_type}")
        if self.current_token.type == token_type:
            if self.peeked_at_token:
                self.current_token = self.peeked_at_token
                self.peeked_at_token = None
            else:
                self.current_token = self.lexer.get_next_token()
        else:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token
            )

    def peek(self):
        if not self.peeked_at_token:
            self.peeked_at_token = self.lexer.get_next_token()
        return self.peeked_at_token

    def parse(self):
        node = self.program()
        if self.current_token.type != TokenType.EOF:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)
        return node

    def program(self):
        if self.current_token.type == TokenType.EOF:
            const = Const(Token(TokenType.STR_CONST, "Hello World!", 2))
            built_in_function = BuiltInFunction('P', [const])
            var_set = VarDecl(0, built_in_function)
            statement_list_node = StatementList()
            statement_list_node.children.append(var_set)
            return Program(statement_list_node)
        statement_list_node = self.statement_list()
        program_node = Program(statement_list_node)
        return program_node

    def statement_list(self):
        root = StatementList()
        root.children.append(self.statement())
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            root.children.append(self.statement())
        return root

    def statement(self):
        if self.current_token.type == TokenType.COLON or self.peek().type == TokenType.COLON:
            return self.function_decl()
        if self.current_token.type == TokenType.IF:
            return self.if_statement()
        if self.current_token.type == TokenType.WHILE:
            return self.while_statement()
        if self.current_token.type == TokenType.RETURN:
            self.eat(TokenType.RETURN)
            self.eat(TokenType.LANGLE)
            node = Return(self.conditional())
            self.eat(TokenType.RANGLE)
            return node
        if self.current_token.type == TokenType.SET:
            return self.var_set()
        if self.current_token.type == TokenType.FUNCTION:
            return self.built_in_function(allow_var_decl=True)
        if self.current_token.type == TokenType.SET_TO:
            self.eat(TokenType.SET_TO)
            return self.var_decl()
        return self.var_decl()

    def var_decl(self):
        return VarDecl(0, self.conditional())

    def var_set(self):
        self.eat(TokenType.SET)
        scope_depth = 0
        while self.current_token.type == TokenType.PERIOD:
            self.eat(TokenType.PERIOD)
            scope_depth += 1
        mem_loc = self.current_token.value
        self.eat(TokenType.INT_CONST)
        self.eat(TokenType.SET_TO)
        return VarSet(scope_depth, mem_loc, self.conditional())

    def function_decl(self):
        params_num = 0
        if self.current_token.type == TokenType.INT_CONST:
            params_num = int(self.current_token.value)
            self.eat(TokenType.INT_CONST)
        self.eat(TokenType.COLON)
        value = self.statement_list()
        self.eat(TokenType.SEMI)
        return VarDecl(params_num, value)

    def if_statement(self):
        self.eat(TokenType.IF)
        conditional = self.conditional()
        self.eat(TokenType.COLON)
        value = self.statement_list()
        self.eat(TokenType.SEMI)
        else_value = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            if self.current_token.type == TokenType.IF:
                else_value = self.if_statement()
            else:
                self.eat(TokenType.COLON)
                else_value = self.statement_list()
                self.eat(TokenType.SEMI)
        return If(conditional, value, else_value)

    def while_statement(self):
        self.eat(TokenType.WHILE)
        conditional = self.conditional()
        self.eat(TokenType.COLON)
        value = self.statement_list()
        self.eat(TokenType.SEMI)
        return While(conditional, value)

    def conditional(self):
        node = self.and_condition()

        while self.current_token.type == TokenType.OR:
            token = self.current_token
            self.eat(TokenType.OR)
            node = BinOp(left=node, op=token, right=self.and_condition())

        return node

    def and_condition(self):
        node = self.condition()

        while self.current_token.type == TokenType.AND:
            token = self.current_token
            self.eat(TokenType.AND)
            node = BinOp(left=node, op=token, right=self.condition())

        return node

    def condition(self):
        invert_result = False
        if self.current_token.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            invert_result = True
        if self.current_token.type == TokenType.LANGLE:
            self.eat(TokenType.LANGLE)
            node = self.conditional()
            self.eat(TokenType.RANGLE)
            return Not(node) if invert_result else node
        else:
            node = self.expr()

            if self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LTHAN, TokenType.GTHAN, TokenType.LTHAN_OR_EQUAL, TokenType.GTHAN_OR_EQUAL):
                token = self.current_token
                if token.type == TokenType.EQUAL:
                    self.eat(TokenType.EQUAL)
                elif token.type == TokenType.NOT_EQUAL:
                    self.eat(TokenType.NOT_EQUAL)
                elif token.type == TokenType.LTHAN:
                    self.eat(TokenType.LTHAN)
                elif token.type == TokenType.GTHAN:
                    self.eat(TokenType.GTHAN)
                elif token.type == TokenType.LTHAN_OR_EQUAL:
                    self.eat(TokenType.LTHAN_OR_EQUAL)
                elif token.type == TokenType.GTHAN_OR_EQUAL:
                    self.eat(TokenType.GTHAN_OR_EQUAL)

                node = BinOp(left=node, op=token, right=self.expr())

            return Not(node) if invert_result else node

    def expr(self):
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        node = self.expo()

        while self.current_token.type in (TokenType.MUL, TokenType.INT_DIV, TokenType.FLOAT_DIV, TokenType.MOD):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.INT_DIV:
                self.eat(TokenType.INT_DIV)
            elif token.type == TokenType.FLOAT_DIV:
                self.eat(TokenType.FLOAT_DIV)
            elif token.type == TokenType.MOD:
                self.eat(TokenType.MOD)

            node = BinOp(left=node, op=token, right=self.expo())

        return node

    def expo(self):
        node = self.factor()

        while self.current_token.type == TokenType.EXPO:
            token = self.current_token
            self.eat(TokenType.EXPO)
            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        token = self.current_token
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            node = UnaryOp(op=token, expr=self.factor())
            return node
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = UnaryOp(op=token, expr=self.factor())
            return node
        elif token.type == TokenType.INT_CONST:
            self.eat(TokenType.INT_CONST)
            return Const(token)
        elif token.type == TokenType.FLOAT_CONST:
            self.eat(TokenType.FLOAT_CONST)
            return Const(token)
        elif token.type == TokenType.STR_CONST:
            self.eat(TokenType.STR_CONST)
            return Const(token)
        elif token.type == TokenType.BOOL_CONST:
            self.eat(TokenType.BOOL_CONST)
            return Const(token)
        elif token.type == TokenType.LANGLE:
            self.eat(TokenType.LANGLE)
            node = self.conditional()
            self.eat(TokenType.RANGLE)
            return node
        elif token.type == TokenType.MEMORY:
            return self.variable()
        elif token.type == TokenType.FUNCTION:
            return self.built_in_function()
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)

    def variable(self):
        self.eat(TokenType.MEMORY)
        scope_depth = 0
        while self.current_token.type == TokenType.PERIOD:
            self.eat(TokenType.PERIOD)
            scope_depth += 1
        mem_loc = self.current_token.value
        self.eat(TokenType.INT_CONST)
        args = []
        if self.current_token.type == TokenType.LANGLE:
            self.eat(TokenType.LANGLE)
            if self.current_token.type != TokenType.RANGLE:
                args.append(self.conditional())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                args.append(self.conditional())
            self.eat(TokenType.RANGLE)
        return VarGet(scope_depth, mem_loc, args)

    def built_in_function(self, allow_var_decl=False):
        def contains_return(f):
            return any(isinstance(node, ast.Return) for node in ast.walk(ast.parse(inspect.getsource(f))))

        token = self.current_token
        self.eat(TokenType.FUNCTION)

        self.eat(TokenType.LANGLE)
        args = []
        if self.current_token.type != TokenType.RANGLE:
            args.append(self.conditional())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                args.append(self.conditional())
        self.eat(TokenType.RANGLE)

        node = BuiltInFunction(token.value, args)

        if allow_var_decl and contains_return(globals()["cs_" + token.value]):
            return VarDecl(0, node)
        return node


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Unspecified file")
    else:
        file_path = sys.argv[1]
        with open(file_path) as file:
            lexer = Lexer(file.read())
        parser = Parser(lexer, True)
        print(parser.parse())
