#!~/.pyenv/shims/python3
# User specific shebang line. Change to your Python interpreter dir

import Lex                  # import Lex.py
from VMConstant import *    # from VMConstant.py import all values

"""

Parser.py parses the .vm file by looking ahead a couple of tokens to determine the type of instruction.
Does not account for source code error or invalid instruction.

"""

class Parser(object):
    def __init__(self, infile):
        self.lex = Lex.Lex(infile)
        self._init_inst_info()

    def _init_inst_info(self):   # helper method for instruction data stores
        self._inst_type = C_ERROR
        self._arg1 = ''
        self._arg2 = 0

    def __str__(self):
        pass

    _null = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not', 'return']    # arithmetic and logical instructions
    _unary = ['label', 'goto', 'if-goto']   # program flow instructions
    _binary = ['push', 'pop', 'function', 'call'] # function calling instructions
    _instruction_type = {       # instruction types
        'add':      C_ARITHMETIC,
        'sub':      C_ARITHMETIC,
        'neg':      C_ARITHMETIC,
        'eq':       C_ARITHMETIC,
        'gt':       C_ARITHMETIC,
        'lt':       C_ARITHMETIC,
        'and':      C_ARITHMETIC,
        'or':       C_ARITHMETIC,
        'not':      C_ARITHMETIC,
        'label':    C_LABEL,
        'goto':     C_GOTO,
        'if-goto':  C_IF,
        'push':     C_PUSH,
        'pop':      C_POP,
        'call':     C_CALL,
        'return':   C_RETURN,
        'function': C_FUNCTION
    }

    def has_more_instructions(self):    # check if more instructions are present
        return self.lex.has_more_instructions()

    def advance(self):      # gets entire line of next instruction
        self._init_inst_info()
        self.lex.next_instruction()
        tok, val = self.lex.curr_token
        if tok != Lex.SYM:          # error
            pass
        if val in self._null:
            self._null_instruction(val)
        elif val in self._unary:
            self._unary_instruction(val)
        elif val in self._binary:
            self._binary_instruction(val)

    def instruction_type(self):         # extracted instruction
        return self._inst_type

    def arg1(self):                     # extracted arg1
        return self._arg1

    def arg2(self):                     # extracted arg2
        return self._arg2

    def _set_inst_type(self, sym):    # parse different instructions
        self._inst_type = self._instruction_type[sym]

    def _null_instruction(self, sym):   # parse null instruction
        self._set_inst_type(sym)
        if self._instruction_type[sym] == C_ARITHMETIC:
            self._arg1 = sym

    def _unary_instruction(self, sym):  # parse unary instruction
        self._null_instruction(sym)
        tok, val = self.lex.next_token()
        self._arg1 = val

    def _binary_instruction(self, sym): # parse binary instruction
        self._unary_instruction(sym)
        tok, val = self.lex.next_token()
        self._arg2 = int(val)
