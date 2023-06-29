from inspect import signature
from types import ModuleType
import builtins
import importlib

from error import *
from cstoken import *
from lexer import *
from csparser import *
from semantic_analyzer import *

from node_visitor import *
from memory import *
from built_in_functions import *


class Function:
    def __init__(self):
        self.return_value = None
        self.has_return_value = False

    def set_return_value(self, return_val):
        self.return_value = return_val
        self.has_return_value = True


class Loop:
    def __init__(self):
        self.breaking = False
        self.continuing = False


class Interpreter(NodeVisitor):
    def __init__(self, file_path, display_debug_messages=False):
        super(Interpreter, self).__init__(display_debug_messages)
        self.current_file_path = file_path
        self.current_scope = None
        self.function_stack = []
        self.loop_stack = []
        self.current_python_module = builtins

    def enter_scope(self, scope_name, enclosing_scope=None):
        enclosing_scope = enclosing_scope if enclosing_scope else self.current_scope
        self.log(f"ENTER scope: {self.current_file_path}: {scope_name}")
        scoped_memory_table = Memory(
            file_path=self.current_file_path,
            scope_name=scope_name,
            scope_level=self.current_scope.scope_level + 1 if self.current_scope else 1,
            enclosing_scope=enclosing_scope,
            scope_to_return_to=self.current_scope,
            display_debug_messages=self.display_debug_messages
        )
        self.current_scope = scoped_memory_table

    def leave_scope(self):
        self.log(self.current_scope)
        self.log(f'LEAVE scope: {self.current_scope.file_path}: {self.current_scope.scope_name}' + f' -> {self.current_scope.scope_to_return_to.file_path}: {self.current_scope.scope_to_return_to.scope_name}' if self.current_scope.scope_to_return_to else '')
        self.current_scope = self.current_scope.scope_to_return_to

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
            return_value = self.visit(child)
            if isinstance(child, Return):
                self.function_stack[-1].set_return_value(return_value)
                break
            if isinstance(child, Break):
                self.loop_stack[-1].breaking = True
                break
            if isinstance(child, Continue):
                self.loop_stack[-1].continuing = True
                break
            if len(self.function_stack) > 0 and self.function_stack[-1].has_return_value:
                self.log(f"Leaving {node.block_type} with return value of {self.function_stack[-1].return_value}")
                break
            if len(self.loop_stack) > 0:
                if self.loop_stack[-1].breaking:
                    self.log(f"Breaking out of {node.block_type}")
                    break
                elif self.loop_stack[-1].continuing:
                    self.log(f"Continuing out of {node.block_type}")
                    break

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = node.op.type
        try:
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
        except:
            self.error(ErrorCode.TYPE_ERROR, node.token, f"'{node.op.value}' not supported between instances of '{type(left).__name__}' and '{type(right).__name__}'")

    def visit_Const(self, node):
        return node.value

    def visit_Null(self, node):
        return None

    def visit_List(self, node):
        return [self.visit(element) for element in node.value]

    def visit_Tuple(self, node):
        return tuple([self.visit(element) for element in node.value])

    def visit_Dict(self, node):
        return {self.visit(key): self.visit(value) for (key, value) in node.value.items()}

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == TokenType.PLUS:
            return self.visit(node.expr)
        if op == TokenType.MINUS:
            return -self.visit(node.expr)

    def visit_VarDecl(self, node):
        # Function
        if isinstance(node.value, StatementList):
            data = FunctionData(node.params_num, node.default_param_vals, node.value)
            self.current_scope.insert(data)
        else:
            value = self.visit(node.value)
            data = Data(value)
            self.current_scope.insert(data)

    def visit_VarSet(self, node):
        value = self.visit(node.value)
        self.current_scope.set(node.scope_depth, node.mem_loc, value)

    def visit_VarGet(self, node):
        if self.current_python_module != builtins:
            self.error(ErrorCode.INVALID_VARIABLE, node.token, f'A CommaScript memory getter cannot be used to get variables/functions from a python module')
        var = self.current_scope.get(node.scope_depth, node.mem_loc)
        if not var:
            self.error(ErrorCode.VARIABLE_MISSING, node.token, f'm{"."*node.scope_depth}{node.mem_loc} seem\'s to have been lost in the darkness that is CommaScript.')
        value = var.value
        # Function
        if isinstance(value, StatementList):
            arg_values = [self.visit(arg) for arg in node.args]

            self.function_stack.append(Function())
            self.enter_scope(f"m{node.mem_loc}", self.current_scope.get_scope(node.scope_depth))

            for default_val in var.default_param_vals[var.params_num - len(arg_values)::]:
                arg_values.append(self.visit(default_val))

            for arg_val in arg_values:
                data = Data(arg_val)
                self.current_scope.insert(data)

            self.visit(value)

            self.leave_scope()
            function = self.function_stack.pop()
            return_value = function.return_value
            return return_value
        # List, Tuple
        elif isinstance(value, (list, tuple)) and node.indexer:
            index = self.visit(node.indexer)
            if not isinstance(index, int) or index < 0 or index >= len(value):
                self.error(ErrorCode.INDEX_ERROR, token=node.token, message=f"{index} is out of range of the given {type(value).__name__}")
            return value[self.visit(node.indexer)]
        # Dictionary
        elif isinstance(value, dict) and node.indexer:
            index = self.visit(node.indexer)
            if index not in value:
                self.error(ErrorCode.INDEX_ERROR, token=node.token, message=f"{index} does not exist in the given dictionary")
            return value[self.visit(node.indexer)]
        elif node.indexer:
            self.error(ErrorCode.INVALID_INDEXER, node.token, f"'{type(value).__name__}' does not support the use of indexers.")
        else:
            return value

    def visit_Import(self, node):
        if node.from_python:
            if node.file_path not in Memory.imported_scopes:
                self.current_scope.import_scope(importlib.import_module(node.file_path))
            self.current_scope.add_imported_scope(node.file_path)
            return

        current_file_path = self.current_file_path
        self.current_file_path = node.file_path

        if node.file_path not in Memory.imported_scopes:
            self.current_scope.import_scope(self.visit(Parser.imported_files[node.file_path]))

        self.current_scope.add_imported_scope(node.file_path)

        self.current_file_path = current_file_path

    def visit_ModuleGet(self, node):
        module = self.current_scope.get_imported_scope(node.scope_depth, node.mem_loc)

        if type(module) is ModuleType:
            self.current_python_module = module
            value = self.visit(node.var_node)
            self.current_python_module = builtins

        else:
            current_scope = self.current_scope
            current_file_path = self.current_file_path
            self.current_scope = module
            self.current_file_path = module.file_path
            self.log(f'ENTER module scope: {self.current_scope.file_path} : {self.current_scope.scope_name}')

            value = self.visit(node.var_node)

            self.log(f'LEAVE module scope: {self.current_scope.file_path} : {self.current_scope.scope_name} -> {current_scope.file_path} : {current_scope.scope_name}')
            self.current_scope = current_scope
            self.current_file_path = current_file_path

        return value

    def visit_OpenFile(self, node):
        mode = 'r' if node.file_mode == TokenType.FILE_READ else 'w' if node.file_mode == TokenType.FILE_WRITE else 'a'
        self.enter_scope("openfile-block")
        with open(node.file_path, mode) as file:
            self.current_scope.insert(Data(file))
            self.visit(node.value)
        self.leave_scope()

    def visit_Not(self, node):
        return not self.visit(node.value)

    def visit_If(self, node):
        if self.visit(node.conditional):
            self.enter_scope("if-block")
            self.visit(node.value)
            self.leave_scope()
        elif node.else_value:
            if isinstance(node.else_value, If):
                self.visit(node.else_value)
            else:
                self.enter_scope("else-block")
                self.visit(node.else_value)
                self.leave_scope()

    def visit_While(self, node):
        loop = Loop()
        self.loop_stack.append(loop)
        while self.visit(node.conditional):
            loop.continuing = False
            self.enter_scope("while-block")
            self.visit(node.value)
            self.leave_scope()
            if (len(self.function_stack) > 0 and self.function_stack[-1].has_return_value or
                    len(self.loop_stack) > 0 and self.loop_stack[-1].breaking):
                break
        self.loop_stack.pop()

    def visit_For(self, node):
        iter = self.visit(node.iterable)
        iter = range(iter) if isinstance(iter, int) else iter
        loop = Loop()
        self.loop_stack.append(loop)
        try:
            for i in iter:
                loop.continuing = False
                self.enter_scope("for-block")
                data = Data(i)
                self.current_scope.insert(data)
                self.visit(node.value)
                self.leave_scope()
                if (len(self.function_stack) > 0 and self.function_stack[-1].has_return_value or
                        len(self.loop_stack) > 0 and self.loop_stack[-1].breaking):
                    break
        except TypeError:
            self.error(ErrorCode.TYPE_ERROR, node.token, f"'{type(iter).__name__}' is not iterable")
        self.loop_stack.pop()

    def visit_Return(self, node):
        return self.visit(node.expr)

    def visit_Break(self, node):
        pass

    def visit_Continue(self, node):
        pass

    def visit_BuiltInFunction(self, node):
        function = getattr(self.current_python_module, node.name) if node.from_python else globals()['cs_' + node.name]
        args = [self.visit(arg) for arg in node.args]
        try:
            if node.from_python:
                return function(*args)
            return function(self, node.token, *args)
        except TypeError:
            self.error(ErrorCode.WRONG_PARAMS_NUM, node.token, f"{node.name}<> takes {len(signature(function).parameters) - 2} arguments but {len(args)} were given")

    def visit_GetAttr(self, node):
        try:
            return getattr(self.current_python_module, node.name)
        except:
            self.error(ErrorCode.INVALID_VARIABLE, node.token, f"'{self.current_python_module}' has no attribute '{node.name}'")

    # def visit_PythonModuleFunction(self, node):
    #     function = getattr(self.current_python_module, node.name)
    #     args = [self.visit(arg) for arg in node.args]
    #     try:
    #         return function(*args)

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
