from token.constants import *
from enum import Enum
import re


class TokenType(Enum):
    Keyword = "Keyword"
    Delimiter = "Delimiter"
    AttributionOperator = "Attribution Operator"
    RelationalOperator = "Relational Operator"
    AdditiveOperator = "Additive Operator"
    MultiplicativeOperator = "Multiplicative Operator"
    Identifier = "Identifier"
    Integer = "Integer"
    Real = "Real"
    Unknown = "Unknown"


class Token():

    def __init__(self, value, line):
        self.line = line
        self.type = _set_token_type()
        self.value = value

    def _set_token_type(self):
        if self.value in KEYWORD:
            return TokenType.Keyword
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
            return TokenType.Real
        elif re.match(INDENTIFIER_PATTERN, self.value):
            return TokenType.Identifier
        else:
            return TokenType.Unknown

    def __str__(self):
        return f"{self.value},{self.type},{self.line}"


class TokenParser():
    def __init__(self, code_lines):
        self.token_list = []
        self.code_lines = code_lines
        self.current_line = 0

    def _add_token(self, token):
        self.token_list.append(token)

    def parse(self):
        """
        For each line of code, parse the line getting the tokens
        """
        for lines in self.code_lines:
            current_position = 0
            while lines[current_position] != '\n':
                # TODO implement parsing logic
                current_position += 1

            self.current_line += 1
