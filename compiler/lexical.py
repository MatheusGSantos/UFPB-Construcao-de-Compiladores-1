import os
import csv
from compiler.token.Token import TokenParser
from compiler.utils import ColoredText

colored = ColoredText()


class Lexical:
    def __init__(self, file):
        self.output_path = os.path.abspath(f"tests/outLex-{file}"[:-3]+"csv")
        self.file_path = os.path.abspath(f"tests/{file}")

    def run(self):
        print(f"{colored.CYAN}TASK:{colored.NORMAL} Running lexical analyzer on file: {self.file_path}")
        try:
            test_file = open(self.file_path, "r")
            code_lines = test_file.readlines()
            code_lines[-1] += "\n"
            token_parser = TokenParser(code_lines)
            token_parser.parse()
            print(f"{colored.GREEN}RESULT:{colored.NORMAL} Finished running lexical analyzer successfully on " 
                  f"file: {self.file_path}")

            with open(self.output_path, "w", newline='') as f_out:
                for err in token_parser.get_errors():
                    print(f"{colored.WARNING}ERROR: {err}{colored.NORMAL}")
                print(f"{colored.CYAN}TASK:{colored.NORMAL} Dumping output to: {self.output_path}")
                token_list = token_parser.get_token_list()
                writer = csv.writer(f_out, delimiter=',')
                writer.writerow(["Token", "Class", "Line"])
                writer.writerows(token_list)
                print(f"{colored.GREEN}RESULT:{colored.NORMAL} Dumped output to: {self.output_path}")

            test_file.close()
        except IOError:
            raise IOError(f"ERROR: Could not locate {self.file_path}.")