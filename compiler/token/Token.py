from compiler.token.constants import *
from enum import Enum
import re
from compiler.utils import CustomQueue, CharArray


class TokenType(str, Enum):
    Keyword = "Keyword"
    Delimiter = "Delimiter"
    AttributionOperator = "Attribution Operator"
    RelationalOperator = "Relational Operator"
    AdditiveOperator = "Additive Operator"
    MultiplicativeOperator = "Multiplicative Operator"
    Identifier = "Identifier"
    Integer = "Integer"
    RealNumber = "Real"
    Boolean = "Boolean"
    TypeIdentifier = "Type"
    Unknown = "Unknown"


class Token:
    def __init__(self, value, line, type=None):
        self.line = line
        self.value = value
        if type:
            self.type = type
        else:
            self.type = self._set_token_type()

    def _set_token_type(self):
        if self.value in KEYWORD:
            return TokenType.Keyword
        elif self.value in VAR_TYPES:
            return TokenType.TypeIdentifier
        elif self.value in BOOLEANS:
            return TokenType.Boolean
        elif self.value in DELIMITER:
            return TokenType.Delimiter
        elif self.value in ATTRIBUTION:
            return TokenType.AttributionOperator
        elif self.value in ADDITIVE:
            return TokenType.AdditiveOperator
        elif self.value in MULTIPLICATIVE:
            return TokenType.MultiplicativeOperator
        elif self.value in RELATIONAL:
            return TokenType.RelationalOperator
        elif re.match(INTEGER_PATTERN, self.value):
            return TokenType.Integer
        elif re.match(REAL_PATTERN, self.value):
            return TokenType.RealNumber
        elif re.match(IDENTIFIER_PATTERN, self.value):
            return TokenType.Identifier
        else:
            return TokenType.Unknown

    def to_list(self):
        return [self.value, self.type, self.line]

    def __str__(self):
        return f"{self.value},{self.type},{self.line}"


class TokenParser:
    _single_char_symbols = SYMBOL.copy()
    _single_char_symbols.remove(">")
    _single_char_symbols.remove(":")
    _single_char_symbols.remove("<")
    _multiple_char_symbols_mapping = {":": ["="], ">": ["="], "<": ["=", ">"]}

    def __init__(self, code_lines):
        self.token_list = []
        self.code_lines = code_lines
        self.current_line_counter = 0
        self.current_token = CharArray()
        self.current_line_queue = CustomQueue()
        self.in_comment = False
        self.errors = []

    def _add_token(self):
        self.token_list.append(
            Token(self.current_token.to_string(), self.current_line_counter).to_list()
        )
        self.current_token.clear()

    def _take_action_whitespace(self, character):
        if character == "\n":
            self.current_line_counter += 1

    def _take_action_comment(self):
        if self.in_comment:
            self.in_comment = False
        else:
            self.in_comment = True

    def _take_action_word(self):
        character = self.current_token.content[0]

        while re.match(r"[a-zA-Z0-9_]", character):
            character = self.current_line_queue.get()
            if re.match(r"[a-zA-Z0-9_]", character):
                self.current_token.append(character)
            else:
                self.current_line_queue.reinsert(character)

    def _take_action_number(self, is_real=False):
        character = self.current_token.content[0]

        while re.match(INTEGER_PATTERN, character):
            character = self.current_line_queue.get()
            if re.match(INTEGER_PATTERN, character):
                self.current_token.append(character)

        if is_real:
            self.current_line_queue.reinsert(character)
        else:
            if character == "." and re.match(
                INTEGER_PATTERN, self.current_line_queue.peek()
            ):
                self.current_token.append(character)
                self._take_action_number(True)
            else:
                self.current_line_queue.reinsert(character)

    def _take_action_symbol(self, character):
        if character in self._single_char_symbols:
            self._add_token()
        else:
            next_character = self.current_line_queue.get()
            if (
                self._multiple_char_symbols_mapping.get(character)
                and next_character in self._multiple_char_symbols_mapping[character]
            ):
                self.current_token.append(next_character)
                self._add_token()
            else:
                self.current_line_queue.reinsert(next_character)
                if next_character not in WHITESPACE:
                    self._add_token()

    def parse(self):
        """
        For each line of code, parse the line getting the tokens
        """
        for line in self.code_lines:
            self.current_line_queue.clear()

            # Populate queue
            for character in line:
                self.current_line_queue.put(character)

            while not self.current_line_queue.empty():
                character = self.current_line_queue.get()

                if self.in_comment and (character != "}"):
                    if character == "\n":
                        self.current_line_counter += 1

                    continue
                else:
                    if character == "{" or character == "}":
                        if self.current_token.length:
                            self._add_token()
                        self._take_action_comment()

                    elif character in WHITESPACE:
                        if self.current_token.length:
                            self._add_token()
                        self._take_action_whitespace(character)

                    elif re.search(r"[a-zA-Z]", character):
                        self.current_token.append(character)
                        self._take_action_word()

                    elif re.search(r"[0-9]", character):
                        self.current_token.append(character)
                        self._take_action_number()

                    elif character in SYMBOL:
                        if self.current_token.length:
                            self._add_token()
                        self.current_token.append(character)
                        self._take_action_symbol(character)
                    else:
                        if self.current_token.length:
                            self._add_token()
                        self.current_token.append(character)
                        self._add_token()
                        self.errors.append(
                            f"Unknown token '{character}' at line {self.current_line_counter}."
                        )

        if self.in_comment:
            self.errors.append("Unfinished comment section")

    def get_errors(self):
        return self.errors

    def get_token_list(self):
        return self.token_list
