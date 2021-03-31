import os
import csv
from compiler.token.Token import TokenParser


class Lexico:
    def __init__(self, file):
        self.output_path = os.path.abspath(f"tests/out-{file}"[:-3]+"csv")
        self.file_path = os.path.abspath(f"tests/{file}")

    def run(self):
        try:
            test_file = open(self.file_path, "r")
            code_lines = test_file.readlines()
            code_lines[-1] += "\n"
            token_parser = TokenParser(code_lines)
            token_parser.parse()

            with open(self.output_path, "w", newline='') as f_out:
                token_list = token_parser.get_token_list()
                writer = csv.writer(f_out, delimiter=',')
                writer.writerow(["Token", "Class", "Line"])
                writer.writerows(token_list)

            test_file.close()
        except IOError:
            raise IOError(f"Could not locate {self.file_path}.")