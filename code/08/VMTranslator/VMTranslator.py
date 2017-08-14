#!~/.pyenv/shims/python3
# User specific shebang line. Change to your Python interpreter dir

import os, os.path, glob, sys   # import os, glob, and sys for file handling
import Parser, CodeWriter       # import Parser.py and CodeWriter.py
from VMConstant import *        # from VMConstant.py import all values

"""

Usage: python VMTranslator.py   or  python VMTranslator.py [filename.vm|dir]
Prompt: "Enter /path/to/filename.vm or /path/to/dir: "
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

def get_files(file_or_dir):
    if file_or_dir.endswith('.vm'):
        return [file_or_dir], file_or_dir.replace('.vm', '.asm')
    else:
        slash = file_or_dir.rfind('/')
        new_infile = file_or_dir[slash+1:]
        return glob.glob(file_or_dir+'/**/*.vm', recursive=True), file_or_dir+'/'+new_infile+'.asm'

if __name__ == '__main__':          # file input handling
    if len(sys.argv) != 2:
        fhand = input("Enter /path/to/filename.vm or /path/to/dir: ")
        format_file = '{}'.format(fhand)
        format_file, outfile = get_files(format_file)
        trans = VMTranslator()
        trans.translate_all(format_file, outfile)
    else:
        infiles, outfile = get_files( sys.argv[1] )
        trans = VMTranslator()
        trans.translate_all(infiles, outfile)

    input("Press any key to exit")
    quit()
