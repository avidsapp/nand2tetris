#!~/.pyenv/shims/python3
# User specific shebang line. Change to your Python interpreter dir

# Attribution: https://github.com/havivha/Nand2Tetris/tree/master/10/JackAnalyzer

import sys, os, os.path, glob
import Parser

"""

Usage: python JackAnalyzer.py   or  python JackAnalyzer.py [filename.vm|dir]
Prompt: "Enter /path/to/filename.jack or /path/to/dir: "
Requirements: Python 3+

JackAnalyzer.py is a syntax analyzer for the Jack language that translates programs written in the Jack language to XML.

"""

class JackAnalyzer(object):
    def __init__(self):
        pass

    def analyze(self, infiles, outfile):
        for infile in infiles:
            Parser.Parser(infile)

def get_files(file_or_dir):
    if file_or_dir.endswith('.jack'):
        return [file_or_dir], file_or_dir.replace('.jack', '.xml')
    else:
        slash = file_or_dir.rfind('/')
        new_infile = file_or_dir[slash+1:]
        return glob.glob(file_or_dir+'/**/*.jack', recursive=True), file_or_dir+'/'+new_infile+'.xml'

if __name__ == '__main__':          # file input handling
    if len(sys.argv) != 2:
        fhand = input("Enter /path/to/filename.jack or /path/to/dir: ")
        format_file = '{}'.format(fhand)
        format_file, outfile = get_files(format_file)
        analyzer = JackAnalyzer()
        analyzer.analyze(format_file, outfile)
    else:
        infiles, outfile = get_files( sys.argv[1] )
        analyzer = JackAnalyzer()
        analyzer.analyze(format_file, outfile)

    input("Press any key to exit")
    quit()
