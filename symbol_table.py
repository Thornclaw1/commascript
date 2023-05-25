from cstoken import *


class Symbol():
    def __init__(self, params_num, value):
        self.params_num = params_num
        self.value = value

    def __str__(self):
        return f"<Symbol(params_num = {self.params_num}, value = {self.value})>"

    __repr__ = __str__


class ScopedSymbolTable(object):
    imported_scopes = {}

    def __init__(self, file_path, scope_name, scope_level, enclosing_scope=None, display_debug_messages=False):
        self._symbols = []
        self.file_path = file_path
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope
        self.display_debug_messages = display_debug_messages
        ScopedSymbolTable.imported_scopes[file_path] = self
        self.imported_file_paths = []

    def __str__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
            ('File path', self.file_path),
            ('Scope name', self.scope_name),
            ('Scope level', self.scope_level),
            ('Enclosing scope',
                self.enclosing_scope.scope_name if self.enclosing_scope else None
             )
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
        lines.append(f"Imported Files : {', '.join([file_name for file_name in self.imported_file_paths])}")
        h2 = 'Scope (Scoped symbol table) contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend([str(symbol) for symbol in self._symbols])
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    __repr__ = __str__

    def log(self, msg):
        if self.display_debug_messages:
            print(msg)

    def insert(self, symbol):
        self.log('Define: %s' % symbol)
        self._symbols.append(symbol)

    def lookup(self, scope_depth, mem_loc):
        self.log(f'Lookup: m{"."*scope_depth}{mem_loc}, (Scope name: {self.scope_name})')
        if scope_depth > 0:
            if self.enclosing_scope is not None:
                return self.enclosing_scope.lookup(scope_depth - 1, mem_loc)
            return None
        if mem_loc < len(self._symbols):
            return self._symbols[mem_loc]

    def set(self, scope_depth, mem_loc, value):
        self.log(f'Set: m{"."*scope_depth}{mem_loc}, (Scope name: {self.scope_name})')
        if scope_depth > 0:
            if self.enclosing_scope is not None:
                self.enclosing_scope.set(scope_depth - 1, mem_loc, value)
        elif mem_loc < len(self._symbols):
            self._symbols[mem_loc].params_num = 0
            self._symbols[mem_loc].value = value

    def length(self):
        return len(self._symbols)

    def import_scope(self, scope):
        self.log(f'Import Module: {scope.file_path}')
        ScopedSymbolTable.imported_scopes[scope.file_path] = scope

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
            return ScopedSymbolTable.imported_scopes[self.imported_file_paths[mem_loc]]
