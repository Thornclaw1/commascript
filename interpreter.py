from error import *
from cstoken import *
from lexer import *
from csparser import *
from semantic_analyzer import *

from node_visitor import *
from memory import *
from built_in_functions import *


class Interpreter(NodeVisitor):
    def __init__(self, file_path, display_debug_messages=False):
        super(Interpreter, self).__init__(display_debug_messages)
        self.current_file_path = file_path
        self.current_scope = None

    def enter_scope(self, scope_name):
        self.log(f"ENTER scope: {scope_name}")
        scoped_memory_table = Memory(
            file_path=self.current_file_path,
            scope_name=scope_name,
            scope_level=self.current_scope.scope_level + 1 if self.current_scope else 1,
            enclosing_scope=self.current_scope,
            display_debug_messages=self.display_debug_messages
        )
        self.current_scope = scoped_memory_table

    def leave_scope(self):
        self.log(self.current_scope)
        self.log(f'LEAVE scope: {self.current_scope.scope_name}')
        self.current_scope = self.current_scope.enclosing_scope

    def error(self, error_code, token, message=''):
        raise InterpreterError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> File: {self.current_file_path}, Line: {token.line}, Column: {token.column}\n{message}'
        )

    def log(self, msg):
        if self.display_debug_messages:
            print(msg)

    def visit_Program(self, node):
        self.enter_scope("global")
        self.visit(node.statement_list_node)
        global_scope = self.current_scope
        self.leave_scope()
        return global_scope

    def visit_StatementList(self, node):
        for child in node.children:
            self.visit(child)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = node.op.type
        if op_type == TokenType.PLUS:
            return left + right
        elif op_type == TokenType.MINUS:
            return left - right
        elif op_type == TokenType.MUL:
            return left * right
        elif op_type == TokenType.EXPO:
            return left ** right
        elif op_type == TokenType.INT_DIV:
            return left // right
        elif op_type == TokenType.FLOAT_DIV:
            return left / right
        elif op_type == TokenType.MOD:
            return left % right
        elif op_type == TokenType.AND:
            return left and right
        elif op_type == TokenType.OR:
            return left or right
        elif op_type == TokenType.EQUAL:
            return left == right
        elif op_type == TokenType.NOT_EQUAL:
            return left != right
        elif op_type == TokenType.LTHAN:
            return left < right
        elif op_type == TokenType.GTHAN:
            return left > right
        elif op_type == TokenType.LTHAN_OR_EQUAL:
            return left <= right
        elif op_type == TokenType.GTHAN_OR_EQUAL:
            return left >= right

    def visit_Const(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == TokenType.PLUS:
            return self.visit(node.expr)
        if op == TokenType.MINUS:
            return -self.visit(node.expr)

    def visit_VarDecl(self, node):
        # Function
        if isinstance(node.value, StatementList):
            data = Data(node.value)
            self.current_scope.insert(data)
        else:
            value = self.visit(node.value)
            data = Data(value)
            self.current_scope.insert(data)

    def visit_VarSet(self, node):
        value = self.visit(node.value)
        self.current_scope.set(node.scope_depth, node.mem_loc, value)

    def visit_VarGet(self, node):
        value = self.current_scope.get(node.scope_depth, node.mem_loc).value
        # Function
        if isinstance(value, StatementList):
            self.enter_scope(f"m{node.mem_loc}")
            for arg in node.args:
                arg_value = self.visit(arg)
                data = Data(arg_value)
                self.current_scope.insert(data)
            for child in value.children:
                return_val = self.visit(child)
                if return_val:
                    break
            self.leave_scope()
            return return_val
        else:
            return value

    def visit_Import(self, node):
        current_file_path = self.current_file_path
        self.current_file_path = node.file_path

        if node.file_path not in Memory.imported_scopes:
            self.current_scope.import_scope(self.visit(Parser.imported_files[node.file_path]))

        self.current_scope.add_imported_scope(node.file_path)

        self.current_file_path = current_file_path

    def visit_ModuleGet(self, node):
        module = self.current_scope.get_imported_scope(node.scope_depth, node.mem_loc)

        current_scope = self.current_scope
        current_file_path = self.current_file_path
        self.current_scope = module
        self.current_file_path = module.file_path

        value = self.visit(node.var_node)

        self.current_scope = current_scope
        self.current_file_path = current_file_path
        return value

    def visit_Not(self, node):
        return not self.visit(node.value)

    def visit_If(self, node):
        if self.visit(node.conditional):
            self.enter_scope("if-block")
            self.visit(node.value)
            self.leave_scope()
        else:
            if isinstance(node.else_value, If):
                self.visit(node.else_value)
            else:
                self.enter_scope("else-block")
                self.visit(node.else_value)
                self.leave_scope()

    def visit_While(self, node):
        while self.visit(node.conditional):
            self.enter_scope("while-block")
            self.visit(node.value)
            self.leave_scope()

    def visit_Return(self, node):
        return self.visit(node.expr)

    def visit_BuiltInFunction(self, node):
        function_name = 'cs_' + node.name
        function = globals()[function_name]
        return function(self, node.args)

    def visit_NoOp(self, node):
        pass

    def visit_NoneType(self, node):
        pass


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Unspecified file")
    else:
        file_path = sys.argv[1]
        file_contents = ""
        with open(file_path) as file:
            file_contents = file.read()

        debug_messages = False
        if len(sys.argv) > 2 and sys.argv[2] == "--debug":
            debug_messages = True

        if debug_messages:
            h = " Parser "
            print(f"\n{'-'*len(h)}\n{h}\n{'-'*len(h)}\n")

        try:
            lexer = Lexer(file_contents)
            parser = Parser(lexer, file_path, debug_messages)
            tree = parser.parse()
        except (ParserError, LexerError) as e:
            print(e.message)
            sys.exit(1)

        if debug_messages:
            h = " Semantic Analyzer "
            print(f"\n{'-'*len(h)}\n{h}\n{'-'*len(h)}\n")

        semantic_analyzer = SemanticAnalyzer(file_path, debug_messages)
        try:
            semantic_analyzer.visit(tree)
        except SemanticError as e:
            print(e.message)
            sys.exit(1)

        if debug_messages:
            h = " Interpreter "
            print(f"\n{'-'*len(h)}\n{h}\n{'-'*len(h)}\n")

        interpreter = Interpreter(file_path, debug_messages)
        try:
            interpreter.visit(tree)
        except InterpreterError as e:
            print(e.message)
            sys.exit(1)
