import sys
import ast
import inspect
import builtins

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


class BlockType(Enum):
    PROGRAM = 'PROGRAM'
    FUNCTION = 'FUNCTION'
    CONDITIONAL = 'CONDITIONAL'
    LOOP = 'LOOP'
    OPEN_FILE = 'OPEN_FILE'
    MACRO = 'MACRO'


class StatementList(AST):
    def __init__(self, block_type):
        self.block_type = block_type
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


class Null(AST):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return f"Null()"
    __repr__ = __str__


class FString(AST):
    def __init__(self, token, portions):
        self.token = token
        self.portions = portions

    def __str__(self):
        return f"FString({self.portions})"
    __repr__ = __str__


class List(AST):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __str__(self):
        return f"List({self.value})"
    __repr__ = __str__


class Tuple(AST):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __str__(self):
        return f"Tuple({self.value})"
    __repr__ = __str__


class Dict(AST):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __str__(self):
        return f"Dict({self.value})"
    __repr__ = __str__


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def __str__(self):
        return f"UnaryOp({self.op.value} {self.expr})"
    __repr__ = __str__


class VarDecl(AST):
    def __init__(self, params_num, default_param_vals, value):
        self.params_num = params_num
        self.default_param_vals = default_param_vals
        self.value = value

    def __str__(self):
        return f"VarDecl({self.params_num}, {self.default_param_vals}, {self.value})"
    __repr__ = __str__


class VarSet(AST):
    def __init__(self, token, scope_depth, mem_loc, value, add_mode):
        self.token = token
        self.scope_depth = scope_depth
        self.mem_loc = mem_loc
        self.value = value
        self.add_mode = add_mode

    def __str__(self):
        return f"VarSet(s{'.'*self.scope_depth}{self.mem_loc}, {self.value}, add_mode:{self.add_mode})"


class VarGet(AST):
    def __init__(self, token, ref, scope_depth, mem_loc, args, indexer):
        self.token = token
        self.ref = ref
        self.scope_depth = scope_depth
        self.mem_loc = mem_loc
        self.args = args
        self.indexer = indexer

    def __str__(self):
        if self.args and self.indexer:
            return f"VarGet({'~'*self.ref}m{'.'*self.scope_depth}{self.mem_loc}, args:{self.args}, indexer:[{self.indexer}])"
        elif self.args:
            return f"VarGet({'~'*self.ref}m{'.'*self.scope_depth}{self.mem_loc}, args:{self.args})"
        elif self.indexer:
            return f"VarGet({'~'*self.ref}m{'.'*self.scope_depth}{self.mem_loc}, indexer:[{self.indexer}])"
        else:
            return f"VarGet({'~'*self.ref}m{'.'*self.scope_depth}{self.mem_loc})"
    __repr__ = __str__


class MacroDecl(AST):
    def __init__(self, token, params_num, default_param_vals, value):
        self.token = token
        self.params_num = params_num
        self.default_param_vals = default_param_vals
        self.value = value

    def __str__(self):
        return f"MacroDecl({self.params_num}, {self.default_param_vals}, {self.value})"
    __repr__ = __str__


class MacroVarGet(AST):
    def __init__(self, token, mem_loc, indexer):
        self.token = token
        self.mem_loc = mem_loc
        self.indexer = indexer

    def __str__(self):
        return f"MacroVarGet({self.mem_loc}, [{self.indexer}])"
    __repr__ = __str__


class Import(AST):
    def __init__(self, token, file_path, from_python=False):
        self.token = token
        self.file_path = file_path
        self.from_python = from_python

    def __str__(self):
        return f"Import({'^'*self.from_python}{self.file_path})"
    __repr__ = __str__


class ModuleGet(AST):
    def __init__(self, token, scope_depth, mem_loc, var_node):
        self.token = token
        self.scope_depth = scope_depth
        self.mem_loc = mem_loc
        self.var_node = var_node

    def __str__(self):
        return f"ModuleGet({'.'*self.scope_depth}{self.mem_loc}, {self.var_node})"
    __repr__ = __str__


class OpenFile(AST):
    def __init__(self, token, file_path, value):
        self.token = token
        self.file_mode = token.type
        self.file_path = file_path
        self.value = value

    def __str__(self):
        return f"OpenFile({self.file_mode}, {self.file_path}, {self.value})"
    __repr__ = __str__


class Not(AST):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __str__(self):
        return f"Not({self.value})"


class If(AST):
    def __init__(self, token, conditional, value, else_value):
        self.token = token
        self.conditional = conditional
        self.value = value
        self.else_value = else_value

    def __str__(self):
        return f"If({self.conditional}, {self.value}, Else: {self.else_value})"
    __repr__ = __str__


class While(AST):
    def __init__(self, token, conditional, value):
        self.token = token
        self.conditional = conditional
        self.value = value

    def __str__(self):
        return f"While({self.conditional}, {self.value})"
    __repr__ = __str__


class For(AST):
    def __init__(self, token, iterable, value):
        self.token = token
        self.iterable = iterable
        self.value = value

    def __str__(self):
        return f"For({self.iterable}, {self.value})"
    __repr__ = __str__


class Return(AST):
    def __init__(self, token, expr):
        self.token = token
        self.expr = expr

    def __str__(self):
        return f"Return({self.expr})"
    __repr__ = __str__


class Break(AST):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return f"Break()"
    __repr__ = __str__


class Continue(AST):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return f"Continue()"
    __repr__ = __str__


class BuiltInFunction(AST):
    def __init__(self, token, ref, args, from_python=False):
        self.token = token
        self.ref = ref
        self.name = token.value
        self.args = args
        self.from_python = from_python

    def __str__(self):
        return f"BuiltInFunction({'~'*self.ref}{'^'*self.from_python}{self.name}, {self.args})"
    __repr__ = __str__


class GetAttr(AST):
    def __init__(self, token):
        self.token = token
        self.name = token.value

    def __str__(self):
        return f"GetAttr({self.name})"
    __repr__ = __str__


class NoOp(AST):
    def __str__(self):
        return f"NoOp()"
    __repr__ = __str__


class Parser():
    imported_files = {}

    def __init__(self, lexer, file_path, display_debug_messages=False):
        self.lexer = lexer
        self.file_path = file_path
        Parser.imported_files[file_path] = None
        self.current_token = self.lexer.get_next_token()
        self.peeked_at_token = None
        self.display_debug_messages = display_debug_messages

    def error(self, error_code, token, message=''):
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f'\u001b[31m{error_code.value} -> File: {self.file_path}, Line: {token.line}, Column: {token.column}\n{message}\u001b[0m'
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
                token=self.current_token,
                message=f"Expected '{token_type.value}' but got '{self.current_token.value}' instead."
            )

    def peek(self):
        if not self.peeked_at_token:
            self.peeked_at_token = self.lexer.get_next_token()
        return self.peeked_at_token

    def contains_return(self, f):
        return any(isinstance(node, ast.Return) for node in ast.walk(ast.parse(inspect.getsource(f))))

    def parse(self):
        node = self.program()
        if self.current_token.type != TokenType.EOF:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token,
                       f"Unexpected character(s) at end of file: {self.current_token.value}")
        Parser.imported_files[self.file_path] = node
        return node

    def program(self):
        if self.current_token.type == TokenType.EOF:
            token = Token(TokenType.FUNCTION, 'p')
            const = Const(Token(TokenType.STR_CONST, "Hello World!"))
            built_in_function = BuiltInFunction(token, False, [const])
            # var_set = VarDecl(0, built_in_function)
            statement_list_node = StatementList(BlockType.PROGRAM)
            statement_list_node.children.append(built_in_function)
            return Program(statement_list_node)
        statement_list_node = self.statement_list(BlockType.PROGRAM)
        program_node = Program(statement_list_node)
        return program_node

    def statement_list(self, block_type):
        root = StatementList(block_type)
        root.children.append(self.statement())
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            if self.current_token.type == TokenType.EOF or self.current_token.type == TokenType.SEMI:
                break
            root.children.append(self.statement())
        return root

    def statement(self):
        token = self.current_token
        if token.type == TokenType.RANGLE:
            return self.macro_decl()
        if token.type in (TokenType.COLON, TokenType.PARAM_SEP) or self.peek().type in (TokenType.COLON, TokenType.PARAM_SEP):
            return self.function_decl()
        if token.type == TokenType.IF:
            return self.if_statement()
        if token.type == TokenType.WHILE:
            return self.while_statement()
        if token.type == TokenType.FOR:
            return self.for_statement()
        if token.type == TokenType.RETURN:
            self.eat(TokenType.RETURN)
            if self.current_token.type == TokenType.LANGLE:
                self.eat(TokenType.LANGLE)
                node = Return(token, self.conditional())
                self.eat(TokenType.RANGLE)
            else:
                node = Return(token, Null(token))
            return node
        if token.type == TokenType.BREAK:
            self.eat(TokenType.BREAK)
            return Break(token)
        if token.type == TokenType.CONTINUE:
            self.eat(TokenType.CONTINUE)
            return Continue(token)
        if token.type == TokenType.IMPORT:
            return self.import_file()
        if token.type == TokenType.SET:
            return self.var_set()
        if token.type in (TokenType.FUNCTION, TokenType.PYTHON) or token.type == TokenType.TILDA and self.peek().type in (TokenType.FUNCTION, TokenType.PYTHON):
            node = self.built_in_function(allow_var_decl=True)
            if self.current_token.type == TokenType.PERIOD:
                return self.factor_method(node.value)
            return node
        if token.type == TokenType.SET_TO:
            self.eat(TokenType.SET_TO)
            return self.var_decl(force_decl=True)
        if token.type == TokenType.NULL and self.peek().type == TokenType.SET_TO:
            self.eat(TokenType.NULL)
            self.eat(TokenType.SET_TO)
            return self.conditional()
        if token.type in (TokenType.FILE_READ, TokenType.FILE_WRITE, TokenType.FILE_APPEND):
            return self.open_file()
        return self.var_decl()

    def import_file(self):
        token = self.current_token
        self.eat(TokenType.IMPORT)

        from_python = False
        if self.current_token.type == TokenType.PYTHON:
            self.eat(TokenType.PYTHON)
            from_python = True

        file_path = self.current_token.value

        if not from_python:
            file_path = file_path + ".cscr" if ".cscr" not in file_path else file_path

            if file_path in Parser.imported_files and not Parser.imported_files[file_path]:
                self.error(ErrorCode.CIRCULAR_IMPORT, token,
                           message=f"importing {file_path} causes a circular import.")

            try:
                with open(file_path) as file:
                    lexer = Lexer(file.read())
            except:
                self.error(error_code=ErrorCode.FILE_NOT_FOUND,
                           token=token, message=f"{file_path} does not exist.")
            parser = Parser(lexer, file_path, self.display_debug_messages)
            self.log('')
            self.log(parser.parse())
            self.log('')

        node = Import(token, file_path, from_python)

        self.eat(TokenType.STR_CONST)
        return node

    def open_file(self):
        token = self.current_token
        if token.type == TokenType.FILE_READ:
            self.eat(TokenType.FILE_READ)
        elif token.type == TokenType.FILE_WRITE:
            self.eat(TokenType.FILE_WRITE)
        elif token.type == TokenType.FILE_APPEND:
            self.eat(TokenType.FILE_APPEND)

        file_path = self.current_token.value
        self.eat(TokenType.STR_CONST)

        self.eat(TokenType.COLON)
        value = self.statement_list(BlockType.OPEN_FILE)
        self.eat(TokenType.SEMI)

        return OpenFile(token, file_path, value)

    def var_decl(self, force_decl=False):
        node = self.conditional()
        if not force_decl and isinstance(node, BuiltInFunction):
            function_name = f"cs_{node.name.lower()}"
            function = globals()[function_name]

            if not self.contains_return(function):
                return node
        return VarDecl(0, [], node)

    def var_set(self):
        token = self.current_token
        self.eat(TokenType.SET)
        scope_depth = 0
        while self.current_token.type == TokenType.PERIOD:
            self.eat(TokenType.PERIOD)
            scope_depth += 1
        if self.current_token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            mem_loc = -self.current_token.value
            self.eat(TokenType.INT_CONST)
        else:
            mem_loc = self.current_token.value
            self.eat(TokenType.INT_CONST)

        value = None
        add_mode = True

        if self.current_token.type in (TokenType.SET_TO, TokenType.PLUS, TokenType.MINUS, TokenType.PLUS_PLUS, TokenType.MINUS_MINUS):
            if self.current_token.type == TokenType.SET_TO:
                self.eat(TokenType.SET_TO)
                value = self.conditional()
                add_mode = False

            elif self.current_token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                value = self.conditional()

            elif self.current_token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                value = UnaryOp(Token(TokenType.MINUS, '-'),
                                self.conditional())

            elif self.current_token.type == TokenType.PLUS_PLUS:
                self.eat(TokenType.PLUS_PLUS)
                value = Const(Token(TokenType.INT_CONST, 1))

            elif self.current_token.type == TokenType.MINUS_MINUS:
                self.eat(TokenType.MINUS_MINUS)
                value = Const(Token(TokenType.INT_CONST, -1))
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN,
                       self.current_token, "Invalid token after set")

        return VarSet(token, scope_depth, mem_loc, value, add_mode)

    def function_decl(self):
        params_num = 0
        if self.current_token.type == TokenType.INT_CONST:
            params_num = int(self.current_token.value)
            self.eat(TokenType.INT_CONST)
        default_param_vals = []
        if self.current_token.type == TokenType.PARAM_SEP:
            self.eat(TokenType.PARAM_SEP)
            if self.current_token.type != TokenType.COLON:
                default_param_vals.append(self.conditional())
                while self.current_token.type != TokenType.COLON:
                    self.eat(TokenType.COMMA)
                    default_param_vals.append(self.conditional())
        self.eat(TokenType.COLON)
        value = self.statement_list(BlockType.FUNCTION)
        self.eat(TokenType.SEMI)
        return VarDecl(params_num, default_param_vals, value)

    def macro_decl(self):
        token = self.current_token
        self.eat(TokenType.RANGLE)
        params_num = 0
        if self.current_token.type == TokenType.INT_CONST:
            params_num = int(self.current_token.value)
            self.eat(TokenType.INT_CONST)
        default_param_vals = []
        if self.current_token.type == TokenType.PARAM_SEP:
            self.eat(TokenType.PARAM_SEP)
            if self.current_token.type != TokenType.COLON:
                default_param_vals.append(self.conditional())
                while self.current_token.type != TokenType.COLON:
                    self.eat(TokenType.COMMA)
                    default_param_vals.append(self.conditional())
        self.eat(TokenType.COLON)
        value = self.statement_list(BlockType.MACRO)
        self.eat(TokenType.SEMI)
        return MacroDecl(token, params_num, default_param_vals, value)

    def if_statement(self):
        token = self.current_token
        self.eat(TokenType.IF)
        conditional = self.conditional()
        self.eat(TokenType.COLON)
        value = self.statement_list(BlockType.CONDITIONAL)
        self.eat(TokenType.SEMI)
        else_value = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            if self.current_token.type == TokenType.IF:
                else_value = self.if_statement()
            else:
                self.eat(TokenType.COLON)
                else_value = self.statement_list(BlockType.CONDITIONAL)
                self.eat(TokenType.SEMI)
        return If(token, conditional, value, else_value)

    def while_statement(self):
        token = self.current_token
        self.eat(TokenType.WHILE)
        conditional = self.conditional()
        self.eat(TokenType.COLON)
        value = self.statement_list(BlockType.LOOP)
        self.eat(TokenType.SEMI)
        return While(token, conditional, value)

    def for_statement(self):
        token = self.current_token
        self.eat(TokenType.FOR)
        iterable = self.conditional()
        self.eat(TokenType.COLON)
        value = self.statement_list(BlockType.LOOP)
        self.eat(TokenType.SEMI)
        return For(token, iterable, value)

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
            not_token = self.current_token
            self.eat(TokenType.NOT)
            invert_result = True

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

        return Not(not_token, node) if invert_result else node

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
        node = self.factor_method()

        while self.current_token.type == TokenType.EXPO:
            token = self.current_token
            self.eat(TokenType.EXPO)
            node = BinOp(left=node, op=token, right=self.factor_method())

        return node

    def factor_method(self, node=None):
        node = node if node else self.factor()
        while self.current_token.type == TokenType.PERIOD:
            method_node = self.method()
            if isinstance(method_node, ModuleGet):
                method_node.var_node.args.insert(0, node)
            else:
                method_node.args.insert(0, node)
            node = method_node
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
        elif token.type == TokenType.BACKTICK:
            return self.f_string()
        elif token.type == TokenType.LBRACKET:
            return self.list()
        elif token.type == TokenType.LPAREN:
            return self.tuple()
        elif token.type == TokenType.LCURLY:
            return self.dict()
        elif token.type == TokenType.LANGLE:
            self.eat(TokenType.LANGLE)
            node = self.conditional()
            self.eat(TokenType.RANGLE)
            return node
        elif token.type == TokenType.MEMORY or self.peek().type == TokenType.MEMORY:
            return self.variable()
        elif token.type == TokenType.MACRO_VAR:
            return self.macro_var()
        elif token.type == TokenType.MODULE:
            return self.module()
        elif token.type in (TokenType.FUNCTION, TokenType.PYTHON) or token.type == TokenType.TILDA and self.peek().type in (TokenType.FUNCTION, TokenType.PYTHON):
            return self.built_in_function()
        elif token.type == TokenType.NULL:
            self.eat(TokenType.NULL)
            return Null(token)
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token,
                       f"Unexpected character(s): {self.current_token.value}")

    def method(self):
        self.eat(TokenType.PERIOD)
        token = self.current_token
        node = None
        if token.type == TokenType.MEMORY or self.peek().type == TokenType.MEMORY:
            node = self.variable()
        elif token.type in (TokenType.FUNCTION, TokenType.PYTHON) or token.type == TokenType.TILDA and self.peek().type in (TokenType.FUNCTION, TokenType.PYTHON):
            node = self.built_in_function()
        elif token.type == TokenType.MODULE:
            node = self.module()
        if not isinstance(node, (VarGet, BuiltInFunction, ModuleGet)):
            self.error(ErrorCode.TYPE_ERROR, token,
                       f"{type(node).__name__} is not a supported method node")
        return node

    def f_string(self):
        token = self.current_token
        portions = []
        self.eat(TokenType.BACKTICK)

        while self.current_token.type != TokenType.BACKTICK:
            if self.current_token.type == TokenType.LCURLY:
                self.eat(TokenType.LCURLY)
                portions.append(self.conditional())
                self.eat(TokenType.RCURLY)
            else:
                portions.append(Const(self.current_token))
                self.eat(TokenType.STR_CONST)

        self.eat(TokenType.BACKTICK)
        return FString(token, portions)

    def list(self):
        token = self.current_token
        elements = []
        self.eat(TokenType.LBRACKET)
        if self.current_token.type != TokenType.RBRACKET:
            elements.append(self.conditional())
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            if self.current_token.type == TokenType.RBRACKET:
                break
            elements.append(self.conditional())
        self.eat(TokenType.RBRACKET)
        return List(token, elements)

    def tuple(self):
        token = self.current_token
        elements = []
        self.eat(TokenType.LPAREN)
        if self.current_token.type != TokenType.RPAREN:
            elements.append(self.conditional())
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            if self.current_token.type == TokenType.RPAREN:
                break
            elements.append(self.conditional())
        self.eat(TokenType.RPAREN)
        return Tuple(token, elements)

    def dict(self):
        token = self.current_token
        kvps = {}
        self.eat(TokenType.LCURLY)
        if self.current_token.type != TokenType.RCURLY:
            key = self.conditional()
            self.eat(TokenType.COLON)
            value = self.conditional()
            kvps[key] = value
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            if self.current_token.type == TokenType.RCURLY:
                break
            key = self.conditional()
            self.eat(TokenType.COLON)
            value = self.conditional()
            kvps[key] = value
        self.eat(TokenType.RCURLY)
        return Dict(token, kvps)

    def variable(self):
        token = self.current_token
        ref = False
        if self.current_token.type == TokenType.TILDA:
            ref = True
            self.eat(TokenType.TILDA)
        self.eat(TokenType.MEMORY)
        scope_depth = 0
        while self.current_token.type == TokenType.PERIOD:
            self.eat(TokenType.PERIOD)
            scope_depth += 1
        if self.current_token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            mem_loc = -self.current_token.value
            self.eat(TokenType.INT_CONST)
        else:
            mem_loc = self.current_token.value
            self.eat(TokenType.INT_CONST)
        args = []
        indexer = None
        if self.current_token.type == TokenType.LANGLE:
            self.eat(TokenType.LANGLE)
            if self.current_token.type != TokenType.RANGLE:
                args.append(self.conditional())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                args.append(self.conditional())
            self.eat(TokenType.RANGLE)
        elif self.current_token.type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET)
            indexer = self.conditional()
            self.eat(TokenType.RBRACKET)
        return VarGet(token, ref, scope_depth, mem_loc, args, indexer)

    def macro_var(self):
        token = self.current_token
        self.eat(TokenType.MACRO_VAR)
        if self.current_token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            mem_loc = -self.current_token.value
            self.eat(TokenType.INT_CONST)
        else:
            mem_loc = self.current_token.value
            self.eat(TokenType.INT_CONST)
        indexer = None
        if self.current_token.type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET)
            indexer = self.conditional()
            self.eat(TokenType.RBRACKET)
        return MacroVarGet(token, mem_loc, indexer)

    def module(self):
        token = self.current_token
        self.eat(TokenType.MODULE)
        scope_depth = 0
        while self.current_token.type == TokenType.PERIOD:
            self.eat(TokenType.PERIOD)
            scope_depth += 1
        if self.current_token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            mem_loc = -self.current_token.value
            self.eat(TokenType.INT_CONST)
        else:
            mem_loc = self.current_token.value
            self.eat(TokenType.INT_CONST)
        if self.current_token.type == TokenType.MEMORY or self.peek().type == TokenType.MEMORY:
            var = self.variable()
        else:
            var = self.python_module_function()
        return ModuleGet(token, scope_depth, mem_loc, var)

    def built_in_function(self, allow_var_decl=False):
        ref = False
        if self.current_token.type == TokenType.TILDA:
            ref = True
            self.eat(TokenType.TILDA)
        from_python = False
        if self.current_token.type == TokenType.PYTHON:
            self.eat(TokenType.PYTHON)
            from_python = True

        token = self.current_token

        self.eat(TokenType.FUNCTION)

        args = []
        if self.current_token.type == TokenType.LANGLE:
            self.eat(TokenType.LANGLE)
            if self.current_token.type != TokenType.RANGLE:
                args.append(self.conditional())
                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    args.append(self.conditional())
            self.eat(TokenType.RANGLE)

        node = BuiltInFunction(token, ref, args, from_python)

        if from_python:
            try:
                getattr(builtins, token.value)
                if allow_var_decl:  # TODO: Look for ways to check if python's built-in function's have return values or not
                    return VarDecl(0, [], node)
                return node
            except AttributeError:
                self.error(ErrorCode.ID_NOT_FOUND, token,
                           f"Python function {token.value}<> does not exist")

        else:
            function_name = f"cs_{token.value.lower()}"
            if function_name not in globals():
                self.error(ErrorCode.ID_NOT_FOUND, token,
                           f"Function {token.value}<> does not exist")
            function = globals()[function_name]

            if allow_var_decl and self.contains_return(function):
                return VarDecl(0, [], node)
            return node

    def python_module_function(self):
        ref = False
        token = self.current_token
        if token.type == TokenType.TILDA:
            ref = True
            self.eat(TokenType.TILDA)
        self.eat(TokenType.FUNCTION)

        if self.current_token.type == TokenType.LANGLE:
            self.eat(TokenType.LANGLE)
            args = []
            if self.current_token.type != TokenType.RANGLE:
                args.append(self.conditional())
                while self.current_token.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
                    args.append(self.conditional())
            self.eat(TokenType.RANGLE)

            node = BuiltInFunction(token, ref, args, True)
        else:
            node = GetAttr(token)

        return node


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Unspecified file")
    else:
        file_path = sys.argv[1]
        with open(file_path) as file:
            lexer = Lexer(file.read())
        parser = Parser(lexer, file_path, True)
        print(parser.parse())
        print(Parser.imported_files)
