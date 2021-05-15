import os
from compiler.token.Token import Token
from compiler.syntactic_methods import SyntacticTree
from compiler.utils import ColoredText

colored = ColoredText()


class Syntactic:
    def __init__(self, file):
        self.file_path = os.path.abspath(f"tests/outLex-{file}"[:-3]+"csv")

    def run(self):
        print(f"{colored.CYAN}TASK:{colored.NORMAL} Running syntactic/semantic analyzer on file: {self.file_path}")
        try:
            test_file = open(self.file_path, "r")
            file_lines = test_file.readlines()[1:]
            token_list = []

            for line in file_lines:
                info = line.split('\t')
                token_list.append(Token(info[0], info[2][:-1], info[1]))

            syntactic_tree = SyntacticTree(token_list)
            syntactic_tree.parse()
            try:
                print(f"{colored.GREEN}RESULT:{colored.NORMAL} Finished running syntactic/semantic analyzer "
                      f"successfully on "
                      f"file: {self.file_path}")
            except Exception as err:
                print(f"{colored.WARNING}ERROR: {err}{colored.NORMAL}")

            test_file.close()

        except IOError:
            raise IOError(f"ERROR: Could not locate {self.file_path}.")
