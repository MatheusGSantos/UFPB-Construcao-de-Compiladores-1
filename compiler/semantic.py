from compiler.utils import ScopeStack


class SemanticAnalyzer:
    def __init__(self):
        self.scope_Stack = ScopeStack()
        self.scope_aux = 0

    def check_aux_and_take_action(self, identifier):
        if not self.scope_aux:
            try:
                self.scope_Stack.push(identifier)
            except Exception as err:
                raise err
        else:
            try:
                if not self.scope_Stack.in_stack(identifier):
                    raise Exception(f"Token '{identifier}' is not declared.")
            except Exception as err:
                raise err
