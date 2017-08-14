#!~/.pyenv/shims/python3
# User specific shebang line. Change to your Python interpreter dir

# Attribution: https://github.com/aalhour/Assembler.hack

import Code, Parser, SymbolTable        # import Code.py, Parser.py, SymoblTable.py modules

"""

Usage: python Assembler.py
Prompt: "Enter /path/to/filename.asm: "
Requirements: Python 3+

Assembler.py reads /path/to/file.asm (hack assembly code) and outputs /path/to/file.hack (hack binary machine code).

The assembly process is implemented in 2 passes. Pass #1 registers labels in the symbol table. Pass #2 registers variables in the symbol table, replaces symbols with respective memory/instruction addresses from the symbol table, then generates binary machine code and writing this code to a .hack text file, one instruction per line.

"""

class Assembler:
    def __init__(self):
        self.symbol_address = 16
        self.symbol_table = SymbolTable.SymbolTable()

    @staticmethod
    def make_hack_file(infile):     # change file extension from to .hack
        if infile.endswith('.asm'):
            return infile.replace('.asm', '.hack')
        else:
            print("The file ", infile, " is not a .asm file")
            quit()

    def _get_address(self, symbol):     # look up symbol address
        if symbol.isdigit():
            return symbol
        else:
            if not self.symbol_table.contains(symbol):
                self.symbol_table.add_entry(symbol, self.symbol_address)
                self.symbol_address += 1
            return self.symbol_table.get_address(symbol)

    def pass0(self, infile):      # 1st pass - determine memory location of labels
        parser = Parser.Parser(infile)
        curr_address = 0
        while parser.has_more_instructions():
            parser.advance()
            inst_type = parser.instruction_type
            if inst_type in [parser.A_INST, parser.C_INST]:
                curr_address += 1
            elif inst_type == parser.L_INST:
                self.symbol_table.add_entry(parser.symbol, curr_address)

    def pass1(self, asm_file, hack_file):       # 2nd pass - write hack code to output file
        parser = Parser.Parser(asm_file)
        with open(hack_file, 'w', encoding='utf-8') as hack_file:
            code = Code.Code()
            while parser.has_more_instructions():
                parser.advance()
                inst_type = parser.instruction_type
                if inst_type == parser.A_INST:
                    hack_file.write(code.gen_a_inst(self._get_address(parser.symbol)) + '\n')
                elif inst_type == parser.C_INST:
                    hack_file.write(code.gen_c_inst(parser.dest, parser.comp, parser.jmp) + '\n')
                elif inst_type == parser.L_INST:
                    pass

    def assemble(self, infile):       # main method
        self.pass0(infile)
        self.pass1(infile, self.make_hack_file(infile))

if __name__ == '__main__':          # file input handling
    fhand = input("Enter /path/to/filename.asm: ")
    formatFile = '{}'.format(fhand)

    try:
        with open(formatFile) as f:
            pass
    except:
        print("The file ", formatFile, " does not exist")
        quit()

    hack_assembler = Assembler()
    hack_assembler.assemble(formatFile)

    input("Press any key to exit")
    quit()
