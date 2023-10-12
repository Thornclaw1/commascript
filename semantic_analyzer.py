import os.path

from error import *
from cstoken import *
from lexer import *
from csparser import *

from node_visitor import *
from symbol_table import *
from built_in_functions import *


class SemanticAnalyzer(NodeVisitor):
    def __init__(self, file_path, display_debug_messages=False):
        super(SemanticAnalyzer, self).__init__(display_debug_messages)
        self.current_file_path = file_path
        self.current_scope = None
        self.current_macro_var_count = 0
        self.block_type_stack = []
        self.in_module_temps = None

    def enter_scope(self, scope_name):
        self.log(f"ENTER scope: {scope_name}")
        scoped_symbol_table = ScopedSymbolTable(
            file_path=self.current_file_path,
            scope_name=scope_name,
            scope_level=self.current_scope.scope_level + 1 if self.current_scope else 1,
            enclosing_scope=self.current_scope,
            display_debug_messages=self.display_debug_messages
        )
        self.current_scope = scoped_symbol_table

    def leave_scope(self):
        self.log(f'LEAVE scope: {self.current_scope.scope_name}')
        self.log(self.current_scope)
        self.current_scope = self.current_scope.enclosing_scope

    def enter_module_scope(self, module):
        self.in_module_temps = (self.current_scope, self.current_file_path)
        self.current_scope = module
        self.current_file_path = module.file_path
        self.log(
            f"ENTER module scope: {self.current_scope.file_path} : {self.current_scope.scope_name}")

    def leave_module_scope(self):
        if self.in_module_temps:
            self.current_scope = self.in_module_temps[0]
            self.current_file_path = self.in_module_temps[1]
            self.log(
                f'LEAVE module scope: {self.current_scope.file_path} : {self.current_scope.scope_name} -> {self.in_module_temps[0]} : {self.in_module_temps[1]}')
            self.in_module_temps = None

    def error(self, error_code, token, message=''):
        self.log(
            f"------------- SCOPE WHEN ERROR -------------\n{self.current_scope}\n------------- SCOPE WHEN ERROR -------------")
        raise SemanticError(
            error_code=error_code,
            token=token,
            message=f'\u001b[31m{error_code.value} -> File: {self.current_file_path}, Line: {token.line}, Column: {token.column}\n{message}\u001b[0m'
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
        self.block_type_stack.append(node.block_type)
        self.log(
            f'ENTER block => stack: {", ".join([block_type.value for block_type in self.block_type_stack])}')
        for child in node.children:
            self.visit(child)
        self.log(
            f'LEAVE block => stack: {", ".join([block_type.value for block_type in self.block_type_stack])}')
        self.block_type_stack.pop()

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Const(self, node):
        pass

    def visit_Null(self, node):
        pass

    def visit_FString(self, node):
        for portion in node.portions:
            self.visit(portion)

    def visit_List(self, node):
        for element in node.value:
            self.visit(element)

    def visit_Tuple(self, node):
        for element in node.value:
            self.visit(element)

    def visit_Dict(self, node):
        for key, value in node.value.items():
            self.visit(key)
            self.visit(value)

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_VarDecl(self, node):
        if isinstance(node.value, StatementList):
            default_param_values = [self.visit(
                val) for val in node.default_param_vals]
            self.enter_scope(f"m{self.current_scope.length() - 1}")
            for _ in range(node.params_num):
                self.current_scope.insert(Symbol(0, 0, None))
            for val in default_param_values:
                self.current_scope.insert(Symbol(0, 0, val))
            self.visit(node.value)
            self.leave_scope()
        else:
            self.visit(node.value)
        self.current_scope.insert(
            Symbol(node.params_num, len(node.default_param_vals), node.value))

    def visit_VarSet(self, node):
        value = self.visit(node.value)
        self.current_scope.set(node.scope_depth, node.mem_loc, value)

    def visit_VarGet(self, node):
        if self.block_type_stack[-1] != BlockType.MACRO:
            symbol = self.current_scope.lookup(node.scope_depth, node.mem_loc)
            if not symbol:
                self.error(error_code=ErrorCode.ID_NOT_FOUND, token=node.token,
                           message=f"m{'.'*node.scope_depth}{node.mem_loc} does not exist")
            if len(node.args) < symbol.params_num or len(node.args) > symbol.params_num + symbol.default_value_num:
                self.error(error_code=ErrorCode.WRONG_PARAMS_NUM, token=node.token,
                           message=f"{len(node.args)} {'was' if len(node.args) == 1 else 'were'} passed, but {symbol.params_num} {'was' if symbol.params_num == 1 else 'were'} expected")
        self.leave_module_scope()
        for arg in node.args:
            self.visit(arg)

    def visit_MacroDecl(self, node):
        self.current_macro_var_count = node.params_num
        for val in node.default_param_vals:
            self.visit(val)
            self.current_macro_var_count += 1
        self.visit(node.value)
        self.current_scope.insert(
            Symbol(node.params_num, len(node.default_param_vals), node.value))
        self.current_macro_var_count = 0

    def visit_MacroVarGet(self, node):
        if self.block_type_stack[-1] != BlockType.MACRO:
            self.error(error_code=ErrorCode.INVALID_MACRO_VARIABLE, token=node.token,
                       message=f"Macro variable getters may not be used outside of macros.")
        else:
            if node.mem_loc >= self.current_macro_var_count or node.mem_loc < -self.current_macro_var_count:
                print(self.current_macro_var_count)
                self.error(error_code=ErrorCode.ID_NOT_FOUND, token=node.token,
                           message=f"k{node.mem_loc} does not exist")

    def visit_Import(self, node):
        if node.from_python:
            if node.file_path not in ScopedSymbolTable.imported_scopes:
                self.current_scope.import_scope(node)
            self.current_scope.add_imported_scope(node.file_path)
            return

        current_file_path = self.current_file_path
        self.current_file_path = node.file_path

        if node.file_path not in ScopedSymbolTable.imported_scopes:
            self.current_scope.import_scope(self.visit(
                Parser.imported_files[node.file_path]))

        self.current_scope.add_imported_scope(node.file_path)

        self.current_file_path = current_file_path

    def visit_ModuleGet(self, node):
        module = self.current_scope.get_imported_scope(
            node.scope_depth, node.mem_loc)

        if not module:
            self.error(ErrorCode.MODULE_NOT_FOUND, node.token,
                       message=f"${'.'*node.scope_depth}{node.mem_loc} does not exist")

        if isinstance(module, Import):
            self.visit(node.var_node)
        else:
            self.enter_module_scope(module)

            self.visit(node.var_node)

            self.leave_module_scope()

    def visit_OpenFile(self, node):
        if node.file_mode != TokenType.FILE_WRITE and not os.path.isfile(node.file_path):
            self.error(error_code=ErrorCode.FILE_NOT_FOUND, token=node.token,
                       message=f"{node.file_path} does not exist.")
        self.enter_scope("openfile-block")
        self.current_scope.insert(Symbol(0, 0, node.file_path))
        self.visit(node.value)
        self.leave_scope()

    def visit_Not(self, node):
        self.visit(node.value)

    def visit_If(self, node):
        self.visit(node.conditional)
        self.enter_scope("if-block")
        self.visit(node.value)
        self.leave_scope()
        if node.else_value:
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

    def visit_For(self, node):
        self.visit(node.iterable)
        self.enter_scope("for-block")
        self.current_scope.insert(Symbol(0, 0, None))
        self.visit(node.value)
        self.leave_scope()

    def visit_Return(self, node):
        if BlockType.FUNCTION not in self.block_type_stack and BlockType.MACRO not in self.block_type_stack:
            self.error(ErrorCode.INVALID_RETURN_STATEMENT, node.token,
                       f'Return Statements should not be declared outside of a function')
        self.visit(node.expr)

    def visit_Break(self, node):
        if BlockType.LOOP not in self.block_type_stack and BlockType.MACRO not in self.block_type_stack:
            self.error(ErrorCode.INVALID_BREAK_STATEMENT, node.token,
                       f'Break Statements should not be declared outside of a loop')

    def visit_Continue(self, node):
        if BlockType.LOOP not in self.block_type_stack and BlockType.MACRO not in self.block_type_stack:
            self.error(ErrorCode.INVALID_CONTINUE_STATEMENT, node.token,
                       f'Continue Statements should not be declared outside of a loop')

    def visit_BuiltInFunction(self, node):
        for arg in node.args:
            self.visit(arg)

    def visit_GetAttr(self, node):
        pass

    # def visit_PythonModuleFunction(self, node):
    #     for arg in node.args:
    #         self.visit(arg)

    def visit_NoOp(self, node):
        pass

    def visit_NoneType(self, node):
        pass


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Unspecified file")
    else:
        file_path = sys.argv[1]
        with open(file_path) as file:
            lexer = Lexer(file.read())
        parser = Parser(lexer, file_path)
        tree = parser.parse()
        print(tree)

        semantic_analyzer = SemanticAnalyzer(
            file_path, display_debug_messages=True)
        try:
            semantic_analyzer.visit(tree)
        except SemanticError as e:
            print(e.message)
            sys.exit(1)
