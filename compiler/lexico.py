import re
import os
from token.Token import *


class lexico():
    def __init__(self):
        self.output = None

    def test(self):
        test_file = open(os.path.abspath("tests/test1.pas"))
        code_lines = test_file.readlines()
        token_parser = TokenParser(code_lines)
        self.output = token_parser.parse()


l = lexico()
l.test()
