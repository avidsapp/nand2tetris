#!~/.pyenv/shims/python3
# User specific shebang line. Change to your Python interpreter dir

"""

SymbolTable.py is a hash-table store used to store and resolve symbols with their associated addresses

"""

class SymbolTable(dict):
    def __init__(self):
        super().__init__()
        self.update({       #pre-defined symbols and memory locations
            'SP':       0,
            'LCL':      1,
            'ARG':      2,
            'THIS':     3,
            'THAT':     4,
            'R0':       0,
            'R1':       1,
            'R2':       2,
            'R3':       3,
            'R4':       4,
            'R5':       5,
            'R6':       6,
            'R7':       7,
            'R8':       8,
            'R9':       9,
            'R10':      10,
            'R11':      11,
            'R12':      12,
            'R13':      13,
            'R14':      14,
            'R15':      15,
            'SCREEN':   0x4000,
            'KBD':      0x6000
        })

    def add_entry(self, symbol, address):   # add symbol to symbol table
        self[symbol] = address

    def contains(self, symbol):        # check if symbol is in the symbol table
        return symbol in self

    def get_address(self, symbol):      # get memore/instruction address of symbol in symbol table
        return self[symbol]
