import sys
from compiler.lexical import Lexical
from compiler.syntactic import Syntactic

if __name__ == "__main__":
	if len(sys.argv) > 1:
		test_file = sys.argv[1]
	else:
		test_file = "test1.pas"
	lexical = Lexical(test_file)
	lexical.run()
	syntactic = Syntactic(test_file)
	syntactic.run()
