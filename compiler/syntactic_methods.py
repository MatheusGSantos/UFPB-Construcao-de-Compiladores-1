from compiler.utils import CustomQueue
from compiler.token.Token import TokenType
from compiler.semantic import SemanticAnalyzer


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
        self.command_list_not_found = False
        self.command_not_found = False
        self.variable_not_found = False
        self.procedure_activation_not_found = False
        self.semantic_analyzer = SemanticAnalyzer()

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
            self.current_token = None
            return False

    def reinsert(self):
        if self.current_token:
            self.token_queue.reinsert(self.current_token)

    def parse(self):
        if self.get_next_token():
            self.program()

    def program(self):
        if self.current_token.value == 'program':
            self.semantic_analyzer.scope_Stack.new_scope()  # new scope

            if self.get_next_token() and self.current_token.type == TokenType.Identifier:
                self.semantic_analyzer.scope_Stack.push(self.current_token.value)  # add identifier to scope stack
                self.semantic_analyzer.scope_Stack.populate_types("program")  # init program id

                if self.get_next_token() and self.current_token.value == ";":
                    self.variable_declarations()
                    self.subprograms_declarations()
                    self.composite_command()
                    if not self.get_next_token() or self.current_token.value != '.':
                        raise Exception("Expected '.' at the end of program.")
                else:
                    raise Exception(f"Expected ';' at line {self.current_line - 1}")
            else:
                raise Exception(f"Expected an identifier at line {self.current_line - 1} after 'program'.")
        else:
            raise Exception(f"Expected 'program' at line {self.current_line - 1}")

    def variable_declarations(self):    # ok
        if self.get_next_token() and self.current_token.value == 'var':
            self.variable_declarations_list()
        else:
            self.reinsert()

    def variable_declarations_list(self):
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
            # if self.current_token:
            #     self.reinsert()
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
        if not self.get_next_token() or self.current_token.type != TokenType.TypeIdentifier:
            raise Exception(f"Expected a type at line {self.current_line - 1}")
        self.semantic_analyzer.scope_Stack.populate_types(self.current_token.value)

    def identifier_list(self):
        if self.get_next_token() and self.current_token.type == TokenType.Identifier:
            try:
                self.semantic_analyzer.check_aux_and_take_action(self.current_token.value)
            except Exception as err:
                raise err
            self.more_identifiers()
        else:
            self.identifier_not_found = True
            self.reinsert()

    def more_identifiers(self):
        if self.get_next_token() and self.current_token.value == ',':
            if self.get_next_token() and self.current_token.type == TokenType.Identifier:
                try:
                    self.semantic_analyzer.check_aux_and_take_action(self.current_token.value)
                except Exception as err:
                    raise err
                self.more_identifiers()
            else:
                raise Exception(f"Expected identifier after ',' at line {self.current_line - 1}")
        else:
            self.reinsert()

    def subprograms_declarations(self):
        self.more_subprograms_declarations()

    def more_subprograms_declarations(self):
        self.subprogram_declaration()
        if self.subprogram_dec_not_found:
            self.subprogram_dec_not_found = False
            return

        if self.get_next_token() and self.current_token.value == ';':
            self.more_subprograms_declarations()
        else:
            raise Exception(f"Expected ';' after subprogram declaration at line {self.current_line - 1}")

    def subprogram_declaration(self):
        if self.get_next_token() and self.current_token.value == 'procedure':
            if self.get_next_token() and self.current_token.type == TokenType.Identifier:
                try:
                    self.semantic_analyzer.check_aux_and_take_action(self.current_token.value)
                except Exception as err:
                    raise err
                self.semantic_analyzer.scope_Stack.populate_types("procedure")  # init procedure id
                self.semantic_analyzer.scope_Stack.new_scope()

                self.arguments()
                if self.get_next_token() and self.current_token.value == ';':
                    self.variable_declarations()
                    self.subprograms_declarations()
                    self.composite_command()
                else:
                    raise Exception(f"Expected ';' at the end of procedure declaration at line {self.current_line - 1}")  
            else:
                raise Exception(f"Expected identifier after 'procedure' at line {self.current_line - 1}")
        else:
            self.subprogram_dec_not_found = True
            self.reinsert()

    def arguments(self):
        if self.get_next_token() and self.current_token.value == '(':
            self.parameter_list()
            if not self.get_next_token() or self.current_token.value != ')':
                raise Exception(f"Expected ')' after parameter list at line {self.current_line - 1}")
        else:
            self.reinsert()
            
    def parameter_list(self):
        self.identifier_list()
        if self.identifier_not_found:
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

    def composite_command(self):
        if self.get_next_token() and self.current_token.value == 'begin':
            self.semantic_analyzer.scope_aux += 1
            self.optional_commands()
            if not self.get_next_token() or self.current_token.value != 'end':
                raise Exception(f"Expected 'end' at line {self.current_line - 1}")

            self.semantic_analyzer.scope_aux -= 1
            if not self.semantic_analyzer.scope_aux:
                try:
                    self.semantic_analyzer.scope_Stack.close_scope()
                except Exception as err:
                    raise err
        else:
            self.reinsert()
            raise Exception(f"Expected 'begin' at line {self.current_line - 1}")
    
    def optional_commands(self):
        self.command_list()
        if self.command_list_not_found:
            self.command_list_not_found = False
            return

    def command_list(self):
        self.command()
        if self.command_not_found:
            self.command_not_found = False
            self.command_list_not_found = True
            return
        self.more_commands()

    def command(self):
        is_token_present = self.get_next_token()
        if not is_token_present:
            self.command_not_found = True
            return

        if self.current_token.value == "if":
            # path 'if expr then command else_part'
            self.expression()
            self.semantic_analyzer.TCS.expression_parse()
            if self.get_next_token() and self.current_token.value == "then":
                self.command()
                if self.command_not_found:
                    raise Exception(f"Expected command after 'then' at line {self.current_line - 1}")
                self.else_part()
                return
            else:
                raise Exception(f"Expected 'then' after expression at line {self.current_line - 1}")

        elif self.current_token.value == "while":
            # path 'while expr do command'
            self.expression()
            self.semantic_analyzer.TCS.expression_parse()
            if self.get_next_token() and self.current_token.value == "do":
                self.command()
                if self.command_not_found:
                    raise Exception(f"Expected command after 'do' at line {self.current_line - 1}")
                return
            else:
                raise Exception(f"Expected 'do' after expression at line {self.current_line - 1}")

        self.reinsert()

        self.variable()
        if self.variable_not_found:
            self.variable_not_found = False
            self.reinsert()
        else:
            self.semantic_analyzer.TCS.expr_append(element=self.semantic_analyzer.scope_Stack.get_type(self.current_token.value),
                                                   member_type="term")  # add to expression
            # path 'var := expr'
            if self.get_next_token() and self.current_token.type == TokenType.AttributionOperator:
                self.semantic_analyzer.TCS.expr_append(element=self.current_token.value,
                                                       member_type="operation")  # add to expression
                self.expression()
                self.semantic_analyzer.TCS.expression_parse()
                return
            else:
                raise Exception(f"Expected ':=' at line {self.current_line - 1}")

        # test procedure_activation
        self.procedure_activation()

        if self.procedure_activation_not_found:
            self.procedure_activation_not_found = False
            self.reinsert()
        else:
            return

        # test composite_command
        try:
            self.composite_command()
        except Exception:
            self.command_not_found = True

    def more_commands(self):
        if self.get_next_token() and self.current_token.value == ';':
            self.command()
            if self.command_not_found:
                raise Exception(f"Expected command after ';' at line {self.current_line - 1}")
            self.more_commands()
        else:
            self.reinsert()

    def else_part(self):
        if self.get_next_token() and self.current_token.value == 'else':
            self.command()
            if self.command_not_found:
                raise Exception(f"Expected command after 'else' at line {self.current_line - 1}")
        else:
            self.reinsert()

    def variable(self):   # ok
        if not self.get_next_token() or self.current_token.type != TokenType.Identifier:
            self.variable_not_found = True
            return

        try:
            self.semantic_analyzer.check_aux_and_take_action(self.current_token.value)
        except Exception as err:
            raise err

    def procedure_activation(self):
        if self.get_next_token() and self.current_token.type == TokenType.Identifier:
            try:
                self.semantic_analyzer.check_aux_and_take_action(self.current_token.value)
            except Exception as err:
                raise err
            self.procedure_continuation()
        else:
            self.procedure_activation_not_found = True

    def procedure_continuation(self):
        if self.get_next_token() and self.current_token.value == '(':
            self.expression_list()
            if not self.get_next_token() or self.current_token.value != ')':
                raise Exception(f"Expected ')' after expression list at line {self.current_line - 1}")

        else:
            self.reinsert()

    def expression_list(self):
        self.expression()
        self.semantic_analyzer.TCS.expression_parse()
        self.more_expressions()

    def more_expressions(self):
        if self.get_next_token() and self.current_token.value == ',':
            self.expression()
            self.semantic_analyzer.TCS.expression_parse()
            self.more_expressions()

    def expression(self):
        self.simple_expression()
        self.expression_continuation()

    def expression_continuation(self):
        if self.get_next_token() and self.current_token.type == TokenType.RelationalOperator:
            self.semantic_analyzer.TCS.expr_append(element=self.current_token.value,
                                                   member_type="operation")  # add to expression
            self.simple_expression()
        else:
            self.reinsert()

    def simple_expression(self):
        if self.get_next_token() and self.current_token.value in ['+', '-']:    # signal
            self.term()
            self.more_simple_expressions()
            return

        self.reinsert()
        self.term()
        self.more_simple_expressions()

    def more_simple_expressions(self):
        if self.get_next_token() and self.current_token.type == TokenType.AdditiveOperator:
            self.semantic_analyzer.TCS.expr_append(element=self.current_token.value, member_type="operation")  # add to expression
            self.term()
            self.more_simple_expressions()
        else:
            self.reinsert()

    def term(self):
        self.factor()
        self.more_terms()

    def more_terms(self):
        if self.get_next_token() and self.current_token.type == TokenType.MultiplicativeOperator:
            self.semantic_analyzer.TCS.expr_append(element=self.current_token.value, member_type="operation")  # add to expression
            self.factor()
            self.more_terms()
        else:
            self.reinsert()

    def factor(self):
        is_token_present = self.get_next_token()
        if not is_token_present:
            raise Exception(f"Expected factor at line {self.current_line - 1}")
        
        if self.current_token.value == "not":
            self.semantic_analyzer.TCS.expr_append(element=self.current_token.value, member_type="operation")  # add to expression
            self.factor()
            return
        
        if self.current_token.value == "(":
            self.semantic_analyzer.TCS.expr_append(element=self.current_token.value, member_type="parentesis")  # add to expression
            self.expression()
            if not self.get_next_token() or self.current_token.value != ')':
                raise Exception(f"Expected ')' after expression at line {self.current_line - 1}")
            self.semantic_analyzer.TCS.expr_append(element=self.current_token.value, member_type="parentesis")  # add to expression
            return

        if self.current_token.type == TokenType.Identifier:
            try:
                self.semantic_analyzer.check_aux_and_take_action(self.current_token.value)
            except Exception as err:
                raise err

            self.semantic_analyzer.TCS.expr_append(element=self.semantic_analyzer.scope_Stack.get_type(self.current_token.value), member_type="term")  # add to expression
            self.factor_continuation()
            return

        if self.current_token.type not in [TokenType.Integer, TokenType.RealNumber, TokenType.Boolean]:
            raise Exception(f"Expected factor at line {self.current_line - 1}. Got {self.current_token.value}.")

        self.semantic_analyzer.TCS.expr_append(
            element={TokenType.Integer: "integer",
                     TokenType.RealNumber: "real",
                     TokenType.Boolean: "boolean"
                     }[self.current_token.type],
            member_type="term")  # add to expression

    def factor_continuation(self):
        if self.get_next_token() and self.current_token.value == '(':
            self.semantic_analyzer.TCS.expr_append(element=self.current_token.value, member_type="parentesis")  # add to expression
            self.expression_list()
            if not self.get_next_token() or self.current_token.value != ')':
                raise Exception(f"Expected ')' the end of expression list at line {self.current_line - 1}")
            self.semantic_analyzer.TCS.expr_append(element=self.current_token.value, member_type="parentesis")  # add to expression
        else:
            self.reinsert()
