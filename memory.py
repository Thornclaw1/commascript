from error import *
from cstoken import *


class Data(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"<Data(value = {self.value}, type = {type(self.value)})>"

    __repr__ = __str__


class Memory(object):
    def __init__(self, scope_name, scope_level, enclosing_scope=None, display_debug_messages=False):
        self._memory = []
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope
        self.display_debug_messages = display_debug_messages
        self.sibling_scopes = []

    def __str__(self):
        h1 = 'SCOPED MEMORY TABLE'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
            ('Scope name', self.scope_name),
            ('Scope level', self.scope_level),
            ('Enclosing scope',
                self.enclosing_scope.scope_name if self.enclosing_scope else None
             )
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
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
            message=f'{error_code.value} -> {token}'
        )

    def log(self, msg):
        if self.display_debug_messages:
            print(msg)

    def insert(self, data):
        self.log('Define: %s' % data)
        self._memory.append(data)

    def get(self, scope_depth, mem_loc):
        self.log(f'Lookup: m{"<"*scope_depth}{mem_loc}, (Scope name: {self.scope_name})')
        if scope_depth > 0:
            if self.enclosing_scope is not None:
                return self.enclosing_scope.get(scope_depth - 1, mem_loc)
            return None
        if mem_loc < len(self._memory):
            return self._memory[mem_loc]

    def set(self, scope_depth, mem_loc, value):
        self.log(f"Set: m{'<'*scope_depth}{mem_loc}, (Scope name: {self.scope_name})")
        if scope_depth > 0:
            if self.enclosing_scope is not None:
                self.enclosing_scope.set(scope_depth - 1, mem_loc, value)
        elif mem_loc < len(self._memory):
            self._memory[mem_loc].value = value

    def add_sibling_scope(self, scope):
        self.log(f"Add Module: {len(self.sibling_scopes)}")
        self.sibling_scopes.append(scope)

    def get_sibling_scope(self, scope_depth, mem_loc):
        self.log(f'Get Module: {mem_loc}')
        if scope_depth > 0:
            if self.enclosing_scope is not None:
                return self.enclosing_scope.get_sibling_scope(scope_depth - 1, mem_loc)
            return None
        if mem_loc < len(self.sibling_scopes):
            return self.sibling_scopes[mem_loc]
