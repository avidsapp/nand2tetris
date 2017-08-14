#!~/.pyenv/shims/python3
# User specific shebang line. Change to your Python interpreter dir

# Attribution: https://github.com/havivha/Nand2Tetris/blob/master/11/JackAnalyzer

import sys, os, os.path, glob
from Parser import *

"""

Usage: python JackAnalyzer.py   or  python JackAnalyzer.py [filename.vm|dir]
Prompt: "Enter /path/to/filename.jack or /path/to/dir: "
Requirements: Python 3+

JackAnalyzer.py is a syntax analyzer for the Jack language that translates programs written in the Jack language to XML.

"""

def analyze(infiles):
    for infile in infiles:
        Parser(infile)

def get_files(file_or_dir):
    if file_or_dir.endswith('.jack'):
        return [file_or_dir]
    else:
        return glob.glob(file_or_dir+'/**/*.jack', recursive=True)

if __name__ == '__main__':          # file input handling
    if len(sys.argv) != 2:
        fhand = input("Enter /path/to/filename.jack or /path/to/dir: ")
        format_file = '{}'.format(fhand)
        infiles = get_files(format_file)
        analyze(infiles)
    else:
        infiles = get_files( sys.argv[1] )
        analyze(infiles)

    input("Press any key to exit")
    quit()
