from compiler.utils import CustomQueue
from compiler.token.Token import TokenType


class SyntacticTree:
    def __init__(self, token_queue=None):
        """

        :type token_queue: CustomQueue|list
        """
        if token_queue:
            if isinstance(token_queue, CustomQueue):
                self.token_queue = token_queue
            elif isinstance(token_queue, list):
                self.token_queue = CustomQueue(token_queue)
            else:
                raise Exception('Invalid argument type: token_queue')
        else:
            self.token_queue = CustomQueue()

        self.current_token = None
        self.current_line = 0
        self.identifier_not_found = False
        self.subprogram_dec_not_found = False

    def set_token_queue(self, src_list):
        if isinstance(src_list, list):
            self.token_queue = src_list
        else:
            raise Exception('Invalid argument type: token_queue')

    def get_next_token(self):
        if not self.token_queue.empty():
            self.current_token = self.token_queue.get()
            self.current_line = int(self.current_token.line)
            return True
        else:
            return False

    def reinsert(self):
        self.token_queue.reinsert(self.current_token)

    def parse(self):
        if self.get_next_token():
            self.program()

    def program(self):
        if self.current_token.value == 'program':
            if self.get_next_token() and self.current_token.type == TokenType.Identifier:
                if self.get_next_token() and self.current_token.value == ";":
                    self.variable_declarations()
                    # self.subprograms_declarations()
                    # self.composite_command()
                    if not self.get_next_token() or self.current_token.value != '.':
                        raise Exception("Expected '.' at the end of program.")
                else:
                    raise Exception(f"Expected ';' at line {self.current_line - 1}")
            else:
                raise Exception(f"Expected an identifier at line {self.current_line - 1} after 'program'.")
        else:
            raise Exception(f"Expected 'program' at line {self.current_line - 1}")

    # base
    def variable_declarations(self):    # ok
        if self.get_next_token() and self.current_token.value == 'var':
            self.variable_declarations_list()
        else:
            self.reinsert()

    def variable_declarations_list(self):    # ok
        self.identifier_list()

        if self.identifier_not_found:
            raise Exception(f"Expected an identifier at line {self.current_line - 1}")

        if self.get_next_token() and self.current_token.value == ':':
            self.type()
            if self.get_next_token() and self.current_token.value == ';':
                self.more_variable_declarations_list()
            else:
                raise Exception(f"Expected ';' at line {self.current_line - 1}")
        else:
            raise Exception(f"Expected ':' at line {self.current_line - 1}")

    def more_variable_declarations_list(self):    # ok
        self.identifier_list()

        if self.identifier_not_found:
            self.identifier_not_found = False
            if self.current_token:
                self.reinsert()
            return

        if self.get_next_token() and self.current_token.value == ':':
            self.type()
            if self.get_next_token() and self.current_token.value == ";":
                self.more_variable_declarations_list()
            else:
                raise Exception(f"Expected ';' after type at line {self.current_line - 1}")
        else:
            raise Exception(f"Expected ':' after identifier at line {self.current_line - 1}")

    def type(self):    # ok
        if not self.get_next_token() or self.current_token.type != TokenType.Type:
            raise Exception(f"Expected a type at line {self.current_line - 1}")

    def identifier_list(self):    # ok
        if self.get_next_token() and self.current_token.type == TokenType.Identifier:
            self.more_identifiers()
        else:
            self.identifier_not_found = True

    def more_identifiers(self):    # ok
        if self.get_next_token() and self.current_token.value == ',':
            if self.get_next_token() and self.current_token.type == TokenType.Identifier:
                self.more_identifiers()
            else:
                raise Exception(f"Expected identifier after ',' at line {self.current_line - 1}")
        else:
            self.reinsert()

    # base
    def subprograms_declarations(self):
        self.more_subprograms_declarations()

    def more_subprograms_declarations(self):
        self.subprogram_declaration()
        if self.subprogram_dec_not_found():
            self.subprogram_dec_not_found = False
            if self.current_token:
                self.reinsert()
            return

        if self.get_next_token() and self.current_token.value == ';':
            self.more_subprograms_declarations()
        else:
            raise Exception(f"Expected ';' after subprogram declaration at line {self.current_line - 1}")

    def subprogram_declaration(self):
        if self.get_next_token() and self.current_token.value == 'procedure':
            if self.get_next_token() and self.current_token.value == 'id':
                self.arguments()
                    if self.get_next_token() and self.current_token.value == ';':
                        self.variable_declarations()
                        self.subprograms_declarations()
                        self.composite_command()

    def arguments(self):
        if self.get_next_token() and self.current_token.value == '(':
            self.parameter_list()
            if not self.get_next_token() or self.current_token.value != ')':
                raise Exception(f"Expected ')' after parameter list at line {self.current_line - 1}")
        else:
            self.reinsert()
            
    def parameter_list(self):
        self.identifier_list()
        if self.identifier_not_found():
            self.identifier_not_found = False
            raise Exception(f"Expected identifier after '(' at line {self.current_line - 1}")

        if self.get_next_token() and self.current_token.value == ':':
            self.type()
            self.more_parameters()
        else:
            raise Exception(f"Expected ':' after identifier at line {self.current_line - 1}")

    def more_parameters(self):
        if self.get_next_token() and self.current_token.value == ';':
            self.identifier_list()
            if self.identifier_not_found:
                raise Exception(f"Expected identifier after ; at line {self.current_line - 1}")

            if self.get_next_token() and self.current_token.value == ":":
                self.type()
                self.more_parameters()
            else:
                raise Exception(f"Expected ':' after identifier at line {self.current_line - 1}")
        else:
            self.reinsert()

    # base
    def composite_command(self):
        if self.get_next_token() and self.current_token.value == 'begin':
            # self.optional_comments()
            if not self.get_next_token() or self.current_token.value != 'end':
                raise Exception(f"Expected 'end' at {self.current_line - 1}")
