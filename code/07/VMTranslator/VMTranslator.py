#!~/.pyenv/shims/python3
# User specific shebang line. Change to your Python interpreter dir

# Attribution: https://github.com/havivha/Nand2Tetris/tree/master/07/VMtranslator

import os, os.path              # import os and os.path for file output handling
import Parser, CodeWriter       # import Parser.py and CodeWriter.py
from VMConstant import *        # from VMConstant.py import all values

"""

Usage: python VMTranslator.py
Prompt: "Enter /path/to/filename.vm: "
Requirements: Python 3+

VMTranslator.py is a partial virtual machine that translates programs written in the VM language into programs written in the Hack assembly language.

"""

class VMTranslator(object):
    def __init__(self):
        pass

    def translate_all(self, infiles, outfile):
        if infiles != []:
            code_writer = CodeWriter.CodeWriter(outfile)
            code_writer.write_init()
            for infile in infiles:
                self._translate(infile, code_writer)
            code_writer.close_file()

    def _translate(self, infile, code_writer):
        parser = Parser.Parser(infile)
        code_writer.set_file_name(os.path.basename(infile))
        while parser.has_more_instructions():
            parser.advance()
            self._gen_code(parser, code_writer)

    def _gen_code(self, parser, code_writer):
        inst = parser.instruction_type()
        if inst == C_ARITHMETIC:
            code_writer.write_arithmetic(parser.arg1())
        elif inst == C_PUSH or inst == C_POP:
            code_writer.write_push_pop(inst, parser.arg1(), parser.arg2())
        elif inst == C_LABEL:
            code_writer.write_label(parser.arg1())
        elif inst == C_GOTO:
            code_writer.write_goto(parser.arg1())
        elif inst == C_IF:
            code_writer.write_if(parser.arg1())
        elif inst == C_FUNCTION:
            code_writer.write_function(parser.arg1(), parser.arg2())
        elif inst == C_RETURN:
            code_writer.write_return()
        elif inst == C_CALL:
            code_writer.write_call(parser.arg1(), parser.arg2())

def get_files(infile):
    if infile.endswith('.vm'):
        return [infile], infile.replace('.vm', '.asm')
    else:
        print("The file ", infile, " is not a .vm file")
        quit()

if __name__ == '__main__':          # file input handling
    fhand = input("Enter /path/to/filename.vm: ")
    format_file = '{}'.format(fhand)

    try:
        with open(format_file) as f:
            pass
    except:
        print("The file ", format_file, " does not exist")
        quit()

    format_file, outfile = get_files(format_file)
    trans = VMTranslator()
    trans.translate_all(format_file, outfile)

    input("Press any key to exit")
    quit()
