from compiler.utils import ScopeStack


class SemanticAnalyzer:
    def __init__(self):
        self.scope_Stack = ScopeStack()
