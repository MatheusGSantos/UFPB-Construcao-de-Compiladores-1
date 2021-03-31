import sys
from compiler.lexico import Lexico

if __name__ == "__main__":
	# test_file = sys.argv[1]
	test_file = "test1.pas"
	lexico = Lexico(test_file)
	lexico.run()