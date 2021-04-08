KEYWORD = [
    "program",
    "var",
    "real",
    "boolean",
    "procedure",
    "begin",
    "end",
    "if",
    "then",
    "else",
    "while",
    "do",
    "not",
]
BOOLEANS = ["True", "False"]
WHITESPACE = [" ", "\t", "\n"]
DELIMITER = [";", ".", ":", "(", ")", ","]
ATTRIBUTION = [":="]
ADDITIVE = ["+", "-", "or"]
MULTIPLICATIVE = ["*", "/", "and"]
RELATIONAL = ["=", ">", "<", "<=", ">=", "<>"]
SYMBOL = ["=", ">", "<", ";", ".", ":", "(", ")", ",", "+", "-", "*", "/"]
INTEGER_PATTERN = r"^[0-9]+$"
REAL_PATTERN = r"^[0-9]+\.[0-9]+$"
IDENTIFIER_PATTERN = r"^[a-zA-Z]([a-zA-Z0-9_])*$"
VAR_TYPES = ["integer", "real", "boolean"]
