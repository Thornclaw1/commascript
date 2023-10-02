from error import *
from cstoken import *


class FunctionData(object):
    def __init__(self, params_num, default_param_vals, value):
        self.params_num = params_num
        self.default_param_vals = default_param_vals
        self.value = value

    def __str__(self):
        return f"<FunctionData(params_num = {self.params_num}, default_param_vals = {self.default_param_vals} value = {self.value}, type = {type(self.value)})>"

    __repr__ = __str__


class MacroData(object):
    def __init__(self, params_num, default_param_vals, value):
        self.params_num = params_num
        self.default_param_vals = default_param_vals
        self.value = value

    def __str__(self):
        return f"<MacroData(params_num = {self.params_num}, default_param_vals = {self.default_param_vals} value = {self.value})"

    __repr__ = __str__


class Data(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"<Data(value = {self.value}, type = {type(self.value)})>"

    __repr__ = __str__


class Memory(object):
    imported_scopes = {}

    def __init__(self, file_path, scope_name, scope_level, enclosing_scope=None, scope_to_return_to=None, display_debug_messages=False):
        self._memory = []
        self.file_path = file_path
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope
        self.scope_to_return_to = scope_to_return_to
        self.display_debug_messages = display_debug_messages
        if file_path not in Memory.imported_scopes:
            self.import_scope(self)
        self.imported_file_paths = []

    def __str__(self):
        h1 = 'SCOPED MEMORY TABLE'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
            ('File path', self.file_path),
            ('Scope name', self.scope_name),
            ('Scope level', self.scope_level),
            ('Enclosing scope',
                self.enclosing_scope.scope_name if self.enclosing_scope else None
             ),
            ('Scope to Return to',
             self.scope_to_return_to.scope_name if self.scope_to_return_to else None)
        ):
            lines.append('%-19s: %s' % (header_name, header_value))
        lines.append(
            f"Imported Files : {', '.join([file_name for file_name in self.imported_file_paths])}")
        h2 = 'Memory contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend([str(data) for data in self._memory])
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    __repr__ = __str__

    def error(self, error_code, token):
        raise InterpreterError(
            error_code=error_code,
            token=token,
            message=f'\u001b[31m{error_code.value} -> {token}\u001b[0m'
        )

    def log(self, msg):
        if self.display_debug_messages:
            print(msg)

    def insert(self, data):
        self.log('Define: %s' % data)
        self._memory.append(data)

    def get(self, scope_depth, mem_loc):
        self.log(
            f'Lookup: m{"."*scope_depth}{mem_loc}, (Scope name: {self.file_path}: {self.scope_name})')
        if scope_depth > 0:
            if self.enclosing_scope is not None:
                return self.enclosing_scope.get(scope_depth - 1, mem_loc)
            return None
        if mem_loc < len(self._memory):
            return self._memory[mem_loc]

    def get_scope(self, scope_depth):
        if scope_depth > 0:
            if self.enclosing_scope is not None:
                return self.enclosing_scope.get_scope(scope_depth - 1)
            return None
        return self

    def set(self, scope_depth, mem_loc, value, add_mode):
        self.log(
            f"Set: m{'.'*scope_depth}{mem_loc}, (Scope name: {self.file_path}: {self.scope_name})")
        if scope_depth > 0:
            if self.enclosing_scope is not None:
                return self.enclosing_scope.set(scope_depth - 1, mem_loc, value, add_mode)
        elif mem_loc < len(self._memory):
            if add_mode:
                try:
                    self._memory[mem_loc].value += value
                except:
                    return (type(self._memory[mem_loc].value), type(value))
            else:
                self._memory[mem_loc].value = value

    def import_scope(self, scope):
        try:
            self.log(f"Import Module {scope.file_path}")
            Memory.imported_scopes[scope.file_path] = scope
        except:
            self.log(f"Import Module {scope.__name__}")
            Memory.imported_scopes[scope.__name__] = scope

    def add_imported_scope(self, file_path):
        self.log(f'Add Module: {file_path}')
        self.imported_file_paths.append(file_path)

    def get_imported_scope(self, scope_depth, mem_loc):
        self.log(f'Get Module: ${"."*scope_depth}{mem_loc}')
        if scope_depth > 0:
            if self.enclosing_scope is not None:
                return self.enclosing_scope.get_imported_scope(scope_depth - 1, mem_loc)
            return None
        if mem_loc < len(self.imported_file_paths):
            return Memory.imported_scopes[self.imported_file_paths[mem_loc]]
