from error import *
from cstoken import *
from lexer import *
from csparser import *

from node_visitor import *
from symbol_table import *

class SemanticAnalyzer(NodeVisitor):
    def __init__(self, display_debug_messages=False):
        super(SemanticAnalyzer, self).__init__(display_debug_messages)
        self.current_scope = None
        self._function_param_nums = {
            TokenType.PRINT : -1,
            TokenType.INPUT : 1,
            TokenType.RANDOM_INT : 2,
            TokenType.CAST_STR : 1,
            TokenType.CAST_INT : 1,
            TokenType.CAST_FLOAT : 1,
            TokenType.CAST_BOOL : 1
        }

    def enter_scope(self, scope_name):
        self.log(f"ENTER scope: {scope_name}")
        scoped_symbol_table = ScopedSymbolTable(
            scope_name=scope_name,
            scope_level=self.current_scope.scope_level + 1 if self.current_scope else 1,
            enclosing_scope=self.current_scope,
            display_debug_messages=self.display_debug_messages
        )
        self.current_scope = scoped_symbol_table

    def leave_scope(self):
        self.log(self.current_scope)
        self.log(f'LEAVE scope: {self.current_scope.scope_name}')
        self.current_scope = self.current_scope.enclosing_scope

    def error(self, error_code, token):
        raise SemanticError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}'
        )

    def log(self, msg):
        if self.display_debug_messages:
            print(msg)

    def visit_Program(self, node):
        self.enter_scope("global")
        self.visit(node.statement_list_node)
        self.leave_scope()

    def visit_StatementList(self, node):
        for child in node.children:
            self.visit(child)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Const(self, node):
        pass

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_VarDecl(self, node):
        self.current_scope.insert(Symbol(node.params_num, node.value))
        if isinstance(node.value, StatementList):
            self.enter_scope(f"m{self.current_scope.length() - 1}")
            for _ in range(node.params_num):
                self.current_scope.insert(Symbol(0, None))
            self.visit(node.value)
            self.leave_scope()
        else:
            self.visit(node.value)

    def visit_VarSet(self, node):
        value = self.visit(node.value)
        self.current_scope.set(node.scope_depth, node.mem_loc, value)

    def visit_VarGet(self, node):
        symbol = self.current_scope.lookup(node.scope_depth, node.mem_loc)
        if not symbol:
            self.error(error_code=ErrorCode.ID_NOT_FOUND, token=node.mem_loc)
        if symbol.params_num != len(node.args):
            self.error(error_code=ErrorCode.WRONG_PARAMS_NUM, token=f"{len(node.args)} {'was' if len(node.args) == 1 else 'were'} passed, but {symbol.params_num} {'was' if symbol.params_num == 1 else 'were'} expected")
        for arg in node.args:
            self.visit(arg)

    def visit_Not(self, node):
        self.visit(node.value)

    def visit_If(self, node):
        self.visit(node.conditional)
        self.enter_scope("if-block")
        self.visit(node.value)
        self.leave_scope()
        if isinstance(node.else_value, If):
            self.visit(node.else_value)
        else:
            self.enter_scope("else-block")
            self.visit(node.else_value)
            self.leave_scope()

    def visit_While(self, node):
        self.visit(node.conditional)
        self.enter_scope("while-block")
        self.visit(node.value)
        self.leave_scope()

    def visit_Return(self, node):
        self.visit(node.expr)

    def visit_BuiltInFunction(self, node):
        func_param_num = self._function_param_nums[node.name]
        if func_param_num != len(node.args) and func_param_num != -1:
            self.error(error_code=ErrorCode.WRONG_PARAMS_NUM, token=f"{len(node.args)} {'was' if len(node.args) == 1 else 'were'} passed, but {symbol.params_num} {'was' if symbol.params_num == 1 else 'were'} expected")
        for arg in node.args:
            self.visit(arg)

    def visit_NoneType(self, node):
        pass


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Unspecified file")
    else:
        file_path = sys.argv[1]
        with open(file_path) as file:
            lexer = Lexer(file.read())
        parser = Parser(lexer)
        tree = parser.parse()
        print(tree)

        semantic_analyzer = SemanticAnalyzer(display_debug_messages=True)
        try:
            semantic_analyzer.visit(tree)
        except SemanticError as e:
            print(e.message)
            sys.exit(1)