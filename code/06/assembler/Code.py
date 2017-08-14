#!~/.pyenv/shims/python3
# User specific shebang line. Change to your Python interpreter dir

"""

Code.py generates bit-strings from parsed instruction parts: dest, comp, jump.
Returns a 16-bit binary instruction string.

"""

class Code:
    def __init__(self):
        pass

    _jump_code = ['', 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']  # jump portion binary - index[n]
    _dest_code = ['', 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']   # dest portion binary - index[n]
    _comp_code = {'0':   '0101010',     # 0x2A      # comp portion binary
                  '1':   '0111111',     # 0x3F      # a = 0
                  '-1':  '0111010',     # 0x3A
                  'D':   '0001100',     # 0x0C
                  'A':   '0110000',     # 0x30
                  '!D':  '0001101',     # 0x0D
                  '!A':  '0110001',     # 0x31
                  '-D':  '0001111',     # 0x0F
                  '-A':  '0110011',     # 0x33
                  'D+1': '0011111',     # 0x1F
                  'A+1': '0110111',     # 0x37
                  'D-1': '0001110',     # 0x0E
                  'A-1': '0110010',     # 0x32
                  'D+A': '0000010',     # 0x02
                  'A+D': '0000010',     # 0x02
                  'D-A': '0010011',     # 0x13
                  'A-D': '0000111',     # 0x07
                  'D&A': '0000000',     # 0x00
                  'A&D': '0000000',     # 0x00
                  'D|A': '0010101',     # 0x15
                  'A|D': '0010101',     # 0x15
                  'M':   '1110000',     # 0x70      # a = 1
                  '!M':  '1110001',     # 0x71
                  '-M':  '1110011',     # 0x73
                  'M+1': '1110111',     # 0x77
                  '1+M': '1110111',     # 0x77
                  'M-1': '1110010',     # 0x72
                  'D+M': '1000010',     # 0x42
                  'M+D': '1000010',     # 0x42
                  'D-M': '1010011',     # 0x53
                  'M-D': '1000111',     # 0x47
                  'D&M': '1000000',     # 0x40
                  'M&D': '1000000',     # 0x40
                  'M|D': '1010101',     # 0x50
                  'D|M': '1010101'}     # 0x50

    def _bits(self, n):     # convert int to binary string
        return bin(int(n))[2:]

    def dest(self, d):      # returns 'dest' binary code
        return self._bits(self._dest_code.index(d)).zfill(3)

    def comp(self, c):      # returns 'comp' binary code
        return self._comp_code[c]

    def jump(self, j):      # returns 'jump' binary code
        return self._bits(self._jump_code.index(j)).zfill(3)

    def gen_a_inst(self, address_value):    # returns A-Instruction binary string from address_value
        return '0' + self._bits(address_value).zfill(15)

    def gen_c_inst(self, dest, comp, jump):      # returns C-Instruction binary string from dest, comp, jump
        return '111' + self.comp(comp) + self.dest(dest) + self.jump(jump)
