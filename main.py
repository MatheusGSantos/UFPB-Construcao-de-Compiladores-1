import os
import sys
from compiler import lexico

if __name__ == "__main__":
	try:
		test_file = open(os.path.join(os.path.normpath("./test"), sys.argv[1]))
		code_lines = test_file.readlines()
		
		lexic = lexico()



	except IOError:
		print("Could not open test file")
