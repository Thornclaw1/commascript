from token import *

class Symbol():
    def __init__(self, params_num, value):
        self.params_num = params_num
        self.value = value
    
    def __str__(self):
        return f"<Symbol(params_num = {self.params_num}, value = {self.value})>"
    
    __repr__ = __str__

class ScopedSymbolTable(object):
    def __init__(self, scope_name, scope_level, enclosing_scope=None, display_debug_messages=False):
        self._symbols = []
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope
        self.display_debug_messages = display_debug_messages

    def __str__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
            ('Scope name', self.scope_name),
            ('Scope level', self.scope_level),
            ('Enclosing scope',
                self.enclosing_scope.scope_name if self.enclosing_scope else None
            )
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
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
        self.log(f'Lookup: m{"<"*scope_depth}{mem_loc}, (Scope name: {self.scope_name})')
        if scope_depth > 0:
            if self.enclosing_scope is not None:
                return self.enclosing_scope.lookup(scope_depth - 1, mem_loc)
            return None
        if mem_loc < len(self._symbols):
            return self._symbols[mem_loc]

    def set(self, scope_depth, mem_loc, value):
        self.log(f'Set: m{"<"*scope_depth}{mem_loc}, (Scope name: {self.scope_name})')
        if scope_depth > 0:
            if self.enclosing_scope is not None:
                self.enclosing_scope.set(scope_depth - 1, mem_loc, value)
        elif mem_loc < len(self._symbols):
            self._symbols[mem_loc].params_num = 0
            self._symbols[mem_loc].value = value

    def length(self):
        return len(self._symbols)