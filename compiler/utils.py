from compiler.token.constants import RELATIONAL


class CustomQueue:
    def __init__(self, src_list=None):
        """

        :type src_list: list
        """
        if src_list:
            if isinstance(src_list, list):
                self.queue = src_list
            else:
                raise Exception('Invalid argument type: src_list')
        else:
            self.queue = []

    def get(self):
        element = self.queue[0]
        self.queue.pop(0)
        return element

    def put(self, element):
        self.queue.append(element)

    def reinsert(self, element):
        self.queue.insert(0, element)

    def peek(self):
        return self.queue[0]

    def empty(self):
        if len(self.queue):
            return False
        else:
            return True

    def clear(self):
        while len(self.queue):
            self.queue.pop()

    def __str__(self):
        return self.queue.__str__()


class CharArray:
    def __init__(self):
        self.content = []
        self.length = 0

    def append(self, element):
        self.content.append(element)
        self.length += 1

    def insert(self, index, element):
        self.content.insert(index, element)
        self.length += 1

    def pop(self, index=None):
        try:
            if index:
                self.content.pop(index)
                self.length -= 1
            else:
                self.content.pop(self.length)
                self.length -= 1
        except IndexError:
            raise IndexError
        except Exception:
            raise Exception("Empty array.")

    def clear(self):
        self.content.clear()
        self.length = 0

    def to_string(self):
        return "".join(self.content)

    def __str__(self):
        return self.content.__str__()


class ScopeStack:
    def __init__(self, scope_mark="$"):
        self.stack = []
        self.length = 0
        self.scope_mark = scope_mark

    def push(self, new_identifier):
        """
        Push 'new_identifier' into stack if 'new_identifier' is not already declared in the current scope

        Raise exception if 'new_identifier' is already declared in the current scope
        :type new_identifier: str
        """
        if not self.length or not self.in_scope(new_identifier):
            self.stack.append(Identifier(new_identifier))
            self.length += 1
        else:
            raise Exception(f"Token '{new_identifier}' already declared in current scope.")

    def pop(self):
        """
        Remove and return last item

        Return None if stack is empty
        """
        if self.length:
            self.length -= 1
            return self.stack.pop()
        return None

    def peek(self):
        return self.stack[-1]

    def new_scope(self):
        self.stack.append(Identifier(self.scope_mark, 'Scope Mark'))
        self.length += 1

    def close_scope(self):
        if not self.length:
            raise Exception(f"Empty stack. Couldn't close the current scope because there's no scope")

        for i in range(self.length, 0, -1):
            if self.pop().value == self.scope_mark:
                return

        raise Exception(f"Stack base is not '{self.scope_mark}'. Couldn't close the current scope")

    def in_scope(self, identifier_value):
        if self.length:
            for i in range(self.length, 0, -1):
                if self.stack[i - 1].value == self.scope_mark:
                    break

                if self.stack[i - 1].value == identifier_value:
                    return True

            if self.stack[0].value == self.scope_mark:
                return False
            else:
                raise Exception(
                    f"Reached stack base. Couldn't find {identifier_value} in the current scope because there's no scope")

        raise Exception(f"Empty stack. Couldn't find {identifier_value} in the current scope because there's no scope")

    def in_stack(self, identifier_value):
        """
        Checks if 'identifier_value' is declared in the scope stack. Return True if it is, False otherwise

        Raise exception if stack base is not a scope mark
        """
        if self.length:
            for i in range(self.length, 0, -1):
                if self.stack[i - 1].value == identifier_value:
                    return True

            if self.stack[0].value == self.scope_mark:
                return False
            else:
                raise Exception(
                    f"Reached stack base. Couldn't find {identifier_value} in the current scope because there's no scope")

        raise Exception(f"Empty stack. Couldn't find {identifier_value} in the current scope because there's no scope")

    def populate_types(self, id_type):
        if self.length:
            for i in range(self.length, 0, -1):
                if self.stack[i - 1].value == self.scope_mark:
                    return True

                if self.stack[i - 1].id_type == '-':
                    self.stack[i - 1].id_type = id_type

    def get_type(self, identifier_value):
        if self.length:
            for i in range(self.length, 0, -1):
                if self.stack[i - 1].value == identifier_value:
                    return self.stack[i - 1].id_type
            raise Exception(
                    f"Reached stack base. Couldn't find {identifier_value} in the current scope")


def arithm_op(op1, op2):
    if op1.value == "integer" and op2.value == "real":
        return "real"
    if op1.value == "integer" and op2.value == "integer":
        return "integer"
    if op1.value == "real" and op2.value == "integer":
        return "real"
    if op1.value == "real" and op2.value == "real":
        return "real"
    raise Exception(f"Expected 'number' and 'number' in arithmetic op. Got {op1.value} and {op2.value}.")


def log_op(op1, op2):
    if op1.value == "boolean" and op2.value == "boolean":
        return "boolean"
    raise Exception(f"Expected 'boolean' and 'boolean' in logical op. Got {op1.value} and {op2.value}.")


def rel_op(op1, op2):
    if op1.value in ["integer", "real"] and op2.value in ["integer", "real"]:
        return "boolean"
    raise Exception(f"Expected 'number' and 'number' in relational op. Got {op1.value} and {op2.value}.")


class TCS:
    """
    Type Control Structure
    """
    RELATIONAL_OPERATION = "Relational Operation"
    LOGICAL_OPERATION = "Logical Operation"
    ARITHMETIC_OPERATION = "Arithmetic Operation"

    relational_operators = ["or", "and", "not"]
    arithmetic_operators = ["+", "-", "*", "/"]
    priorities = {
        "+": 3,
        "-": 3,
        "*": 4,
        "/": 4,
        "rel": 2,
        "log": 1
    }

    def __init__(self):
        self.current_expression = []    # keeps current expression
        self.priority_array = []      # priority
        self.current_parentesis_counter = 0

    def expr_append(self, element, member_type):
        """

        :param element: Type value, operation value or parentesis
        :param member_type: "operation" | "parentesis" | "term"
        """
        self.current_expression.append(ExpressionMember(element, member_type))

    def expr_pop(self, pos):
        return self.current_expression.pop(pos)

    def expression_parse(self):
        i = 0
        while i < len(self.current_expression):
            if self.current_expression[i].value == '(':
                self.current_parentesis_counter += 1
                self.expr_pop(i)
                i -= 1
            elif self.current_expression[i].value == ')':
                self.current_parentesis_counter -= 1
                self.expr_pop(i)
                i -= 1
            elif self.current_expression[i].member_type == 'operation':
                self.define_priority_and_push(i)
            i += 1

        self.priority_array.sort(key=take_first, reverse=True)    # sort priorities

        while len(self.priority_array) > 0:
            current_operation = self.priority_array.pop(0)
            op2 = self.expr_pop(current_operation[2]+1)     # operand2
            operation = self.expr_pop(current_operation[2])     # operation
            if operation.value == "not":
                op2.value = "boolean"
                self.current_expression.insert(current_operation[2], op2)  # insert result into expression
                for elem in self.priority_array:  # decrease pos by 1 if pos > current_op pos
                    if elem[2] > current_operation[2]:
                        elem[2] -= 1
            else:
                op1 = self.expr_pop(current_operation[2] - 1)   # operand1

                resultant_type = self.operate(op1, operation, op2)
                op1.value = resultant_type
                self.current_expression.insert(current_operation[2]-1, op1)     # insert result into expression
                for elem in self.priority_array:    # decrease pos by 2 if pos > current_op pos
                    if elem[2] > current_operation[2]:
                        elem[2] -= 2

        self.current_expression = []

    def define_priority_and_push(self, position):
        if self.current_expression[position].value in self.arithmetic_operators:
            self.current_expression[position].member_type = self.ARITHMETIC_OPERATION
            self.priority_array.append([
                self.priorities[self.current_expression[position].value] + (10*self.current_parentesis_counter),
                self.current_expression[position].value,
                position,
            ])
        elif self.current_expression[position].value in self.relational_operators:
            self.current_expression[position].member_type = self.LOGICAL_OPERATION
            self.priority_array.append([
                self.priorities["log"] + (10*self.current_parentesis_counter),
                self.current_expression[position].value,
                position,
            ])
        elif self.current_expression[position].value in RELATIONAL:
            self.current_expression[position].member_type = self.RELATIONAL_OPERATION
            if self.current_expression[position].value == "not":
                self.priority_array.append([
                    self.priorities["rel"] + 5 + (10 * self.current_parentesis_counter),
                    self.current_expression[position].value,
                    position,
                ])
            else:
                self.priority_array.append([
                    self.priorities["rel"] + (10 * self.current_parentesis_counter),
                    self.current_expression[position].value,
                    position,
                ])
        else:
            self.current_expression[position].member_type = "Attribution"
            self.priority_array.append([
                0,
                self.current_expression[position].value,
                position,
            ])

    def operate(self, op1, operation, op2):
        """

        :type op2: ExpressionMember
        :type operation: ExpressionMember
        :type op1: ExpressionMember
        """
        if operation.member_type == "Attribution":
            if op1.value != op2.value:
                raise Exception(f"Could not assign {op2.value} to {op1.value}. Type does not match.")
            return op1.value
        else:
            return self.check_type_out(op1, op2, operation)

    def check_type_out(self, op1, op2, operation):
        if operation.member_type == self.ARITHMETIC_OPERATION:
            return arithm_op(op1, op2)
        if operation.member_type == self.RELATIONAL_OPERATION:
            return rel_op(op1, op2)
        if operation.member_type == self.LOGICAL_OPERATION:
            return log_op(op1, op2)


class ExpressionMember:
    def __init__(self, value, member_type):
        self.value = value
        self.member_type = member_type


class Identifier:
    def __init__(self, value, id_type='-'):
        self.value = value
        self.id_type = id_type


class ColoredText:
    WARNING = '\033[91m'
    NORMAL = '\033[0m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'


def take_first(elem):
    return elem[0]

