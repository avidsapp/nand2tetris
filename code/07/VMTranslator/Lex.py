#!~/.pyenv/shims/python3
# User specific shebang line. Change to your Python interpreter dir

import re       # import Regular Expression module

NUM = 1     # Number constant - '123...'
SYM = 2     # Symbol constant - 'LOOP'
ERR = 3     # Error constant

"""

Lex.py is the same lexer from 06/assembler/, but only detects numbers and symbols
Reads the whole .vm file into memory and uses regex to match lexical tokens

"""

class Lex(object):
    def __init__(self, infile):
        fhand = open(infile, 'r')
        self._lines = fhand.read()
        self._tokens = self._tokenize(self._lines.split('\n'))
        self.curr_instruction = []      # list of tokens for current instruction
        self.curr_token = (ERR, 0)      # current token of current instruction

    def __str__(self):
        pass

    # regex patterns
    _num_re = r'\d+'        # number regex pattern
    _sym_re = r'[\w\-.]+'   # symbol regex pattern
    _word = re.compile(_num_re + '|' + _sym_re) # compile word pattern into an object for matching using bitwise OR
    _comment = re.compile('//.*$')      # compile comment pattern into an object for matching

    def _is_match(self, pattern, word):     # checks if input regex pattern matches word
        return re.match(pattern, word) != None

    def _is_number(self, word):             # checks if word is a number
        return self._is_match(self._num_re, word)

    def _is_symbol(self, word):             # checks if word is a symbol
        return self._is_match(self._sym_re, word)

    def _remove_comment(self, line):        # removes comment from line
        return self._comment.sub('', line)

    def _token(self, word):     # assigns word a token constant
        if self._is_number(word):
            return (NUM, word)
        elif self._is_symbol(word):
            return (SYM, word)
        else:
            return (ERR, word)

    def _split(self, line):     # return matches of word object in line
        return self._word.findall(line)

    def _tokenize_line(self, line):        # tokenize line before comment, if present
        return [self._token(word) for word in self._split(self._remove_comment(line))]

    def _tokenize(self, lines):         # tokenize all lines
        return [t for t in [self._tokenize_line(l) for l in lines] if t!=[]]

    def has_more_instructions(self):    # if more tokens are present, there are more instructions
        return self._tokens != []

    def next_instruction(self):         # pop first token from stack and move to next token
        self.curr_instruction = self._tokens.pop(0)
        self.next_token()
        return self.curr_instruction

    def has_next_token(self):           # if next_instruction finds a token, there are more tokens
        return self.curr_instruction != []

    def next_token(self):       # move to next token
        if self.has_next_token():
            self.curr_token = self.curr_instruction.pop(0)
        else:
            self.curr_token = ERR, 0
        return self.curr_token

    def peek_token(self):       # look ahead to the next tokens, return error if no next token
        if self.has_next_token():
            return self.curr_instruction[0]
        else:
            return (ERR, 0)
