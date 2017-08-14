#!~/.pyenv/shims/python3
# User specific shebang line. Change to your Python interpreter dir

import Lex      # import Lex.py module

"""

Parser.py parses the .asm file by looking ahead a couple of tokens to determine the type of instruction.
Does not account for source code error or invalid instruction.

"""

class Parser:
    def __init__(self, infile):
        self.lex = Lex.Lex(infile)
        self._init_instruction_info()

    def _init_instruction_info(self):   # helper method for instruction data stores
        self._instruction_type = -1
        self._symbol = ''
        self._dest = ''
        self._comp = ''
        self._jmp = ''

    def __str__(self):
        pass

    A_INST = 0      # addressing instruction constant
    C_INST = 1      # computation instruction constant
    L_INST = 2      # label-declaration constant

    def has_more_instructions(self):    # check if more instructions are present
        return self.lex.has_more_instructions()

    def advance(self):      # gets entire line of next instruction
        self._init_instruction_info()
        self.lex.next_instruction()
        token, val = self.lex.curr_token
        if token == Lex.OPR and val == '@':
            self._a_instruction()
        elif token == Lex.OPR and val == '(':
            self._l_instruction()
        else:
            self._c_instruction(token, val)

    def _a_instruction(self):       # examples: @64, @n, @LOOP
        self._instruction_type = Parser.A_INST
        tok_type, self._symbol = self.lex.next_token()

    def _l_instruction(self):       # examples: (END), (LOOP)
        self._instruction_type = Parser.L_INST
        tok_type, self._symbol = self.lex.next_token()

    """
    Computation
        dest=comp;jump
        dest=comp           omit jump
        comp;jump           omit dest
        comp                omit dest and jump
    """
    def _c_instruction(self, token, value):
        self._instruction_type = Parser.C_INST
        comp_tok, comp_val = self._get_dest(token, value)
        self._get_comp(comp_tok, comp_val)
        self._get_jump()

    def _get_dest(self, token, value):   # get 'dest' if any, return first 'comp' token
        tok2, val2 = self.lex.peek_token()
        if tok2 == Lex.OPR and val2 == '=':
            self.lex.next_token()
            self._dest = value
            comp_tok, comp_val = self.lex.next_token()
        else:
            comp_tok, comp_val = token, value
        return comp_tok, comp_val

    def _get_comp(self, token, value):  # get 'comp'
        if token == Lex.OPR and (value == '-' or value == '!'):
            tok2, val2 = self.lex.next_token()
            self._comp = value + val2
        elif token == Lex.NUM or token == Lex.SYM:
            self._comp = value
            tok2, val2 = self.lex.peek_token()
            if tok2 == Lex.OPR and val2 != ';':
                self.lex.next_token()
                tok3, val3 = self.lex.next_token()
                self._comp += val2+val3

    def _get_jump(self):    #get jump
        token, value = self.lex.next_token()
        if token == Lex.OPR and value == ';':
            jump_tok, jump_val = self.lex.next_token()
            self._jmp = jump_val

    @property
    def instruction_type(self):     # extracted instruction type
        return self._instruction_type

    @property
    def symbol(self):               # extracted symbol
        return self._symbol

    @property
    def dest(self):                 # extracted 'dest'
        return self._dest

    @property
    def comp(self):                 # extracted 'comp'
        return self._comp

    @property
    def jmp(self):                  # extracted 'jmp'
        return self._jmp
