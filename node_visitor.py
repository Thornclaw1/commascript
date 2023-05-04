class NodeVisitor(object):
    def __init__(self, display_debug_messages=False):
        self.display_debug_messages = display_debug_messages

    def visit(self, node):
        if self.display_debug_messages:
            print(f"VISITING {type(node).__name__}")
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')