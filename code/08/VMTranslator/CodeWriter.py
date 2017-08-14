#!~/.pyenv/shims/python3
# User specific shebang line. Change to your Python interpreter dir

import os, os.path
from VMConstant import *

'''

CodeWriter.py translates VM instructions into Hack assembly code

'''

class CodeWriter(object):
    def __init__(self, outfile):
        self._out_file = open(outfile, 'w')
        self._vm_file = ''
        self._labelnum = 0

    def __str__(self):
        pass

    def set_file_name(self, filename):
        self._vm_file, ext = os.path.splitext(filename)

    def close_file(self):
        self._out_file.close()

    def write_init(self):
        self._a_instruction('256')
        self._c_instruction('D', 'A')
        self._comp_to_reg(R_SP, 'D')    # SP = 256
        self.write_call('Sys.init', 0)  # call Sys.init

    def write_arithmetic(self, instruction):
        if      instruction == 'add':
            self._binary('D+A')
        elif    instruction == 'sub':
            self._binary('A-D')
        elif    instruction == 'neg':
            self._unary('-D')
        elif    instruction == 'eq':
            self._compare('JEQ')
        elif    instruction == 'gt':
            self._compare('JGT')
        elif    instruction == 'lt':
            self._compare('JLT')
        elif    instruction == 'and':
            self._binary('D&A')
        elif    instruction == 'or':
            self._binary('D|A')
        elif    instruction == 'not':
            self._unary('!D')

    def write_push_pop(self, instruction, seg, index):
        if      instruction == C_PUSH:
            self._push(seg, index)
        elif    instruction == C_POP:
            self._pop(seg, index)

    def write_label(self, label):
        self._l_instruction(label)

    def write_goto(self, label):
        self._a_instruction(label)              # A=label
        self._c_instruction(None, '0', 'JMP')   # 0;JMP

    def write_if(self, label):
        self._pop_to_dest('D')                  # D=*SP
        self._a_instruction(label)              # A=label
        self._c_instruction(None, 'D', 'JNE')   # D;JNE

    def write_call(self, function_name, num_args):
        return_address = self._new_label()
        self._push(S_CONST, return_address)     # push return_address
        self._push(S_REG, R_LCL)                # push LCL
        self._push(S_REG, R_ARG)                # push ARG
        self._push(S_REG, R_THIS)               # push THIS
        self._push(S_REG, R_THAT)               # push THAT
        self._load_sp_offset(-num_args-5)
        self._comp_to_reg(R_ARG, 'D')           # ARG=SP-n-5
        self._reg_to_reg(R_LCL, R_SP)           # LCL=SP
        self._a_instruction(function_name)      # A=function_name
        self._c_instruction(None, '0', 'JMP')   # 0;JMP
        self._l_instruction(return_address)     # return_address

    def write_return(self):
        self._reg_to_reg(R_FRAME, R_LCL)        # R_FRAME = R_LCL
        self._a_instruction('5')                # A=5
        self._c_instruction('A', 'D-A')         # A=FRAME-5
        self._c_instruction('D', 'M')           # D=M
        self._comp_to_reg(R_RET, 'D')           # RET=*(FRAME-5)
        self._pop(S_ARG, 0)                     # *ARG=return value
        self._reg_to_dest('D', R_ARG)           # D=ARG
        self._comp_to_reg(R_SP, 'D+1')          # SP=ARG+1
        self._prev_frame_to_reg(R_THAT)         # THAT=*(FRAME-1)
        self._prev_frame_to_reg(R_THIS)         # THIS=*(FRAME-2)
        self._prev_frame_to_reg(R_ARG)          # ARG=*(FRAME-3)
        self._prev_frame_to_reg(R_LCL)          # LCL=*(FRAME-4)
        self._reg_to_dest('A', R_RET)           # A=RET
        self._c_instruction(None, '0', 'JMP')   # goto RET

    def _prev_frame_to_reg(self, reg):
        self._reg_to_dest('D', R_FRAME)         # D=FRAME
        self._c_instruction('D', 'D-1')         # D=FRAME-1
        self._comp_to_reg(R_FRAME, 'D')         # FRAME=FRAME-1
        self._c_instruction('A', 'D')           # A=FRAME-1
        self._c_instruction('D', 'M')           # D=*(FRAME-1)
        self._comp_to_reg(reg, 'D')             # reg=D

    def write_function(self, function_name, num_locals):
        self._l_instruction(function_name)
        for i in range(num_locals):
            self._push(S_CONST, 0)

    def _push(self, seg, index):        # generate code for push
        if   self._is_const_seg(seg):
            self._val_to_stack(str(index))
        elif self._is_mem_seg(seg):
            self._mem_to_stack(self._asm_mem_seg(seg), index)
        elif self._is_reg_seg(seg):
            self._reg_to_stack(seg, index)
        elif self._is_static_seg(seg):
            self._static_to_stack(seg, index)
        self._inc_sp()

    def _pop(self, seg, index):         # generate code for pop
        self._dec_sp()
        if   self._is_mem_seg(seg):
            self._stack_to_mem(self._asm_mem_seg(seg), index)
        elif self._is_reg_seg(seg):
            self._stack_to_reg(seg, index)
        elif self._is_static_seg(seg):
            self._stack_to_static(seg, index)


    def _pop_to_dest(self, dest):
        self._dec_sp()
        self._stack_to_dest(dest)       # dest=*SP

    def _is_mem_seg(self, seg):         # memory segment
        return seg in [S_LCL, S_ARG, S_THIS, S_THAT]

    def _is_reg_seg(self, seg):         # register segment
        return seg in [S_REG, S_PTR, S_TEMP]

    def _is_static_seg(self, seg):      # static segment
        return seg == S_STATIC

    def _is_const_seg(self, seg):       # constant segment
        return seg == S_CONST

    def _unary(self, comp):             # unary operation
        self._dec_sp()                      # --SP
        self._stack_to_dest('D')            # D=*SP
        self._c_instruction('D', comp)      # D=COMP
        self._comp_to_stack('D')            # *SP=D
        self._inc_sp()                      # ++SP

    def _binary(self, comp):            # binary operation
        self._dec_sp()                      # --SP
        self._stack_to_dest('D')            # D=*SP
        self._dec_sp()                      # --SP
        self._stack_to_dest('A')            # A=*SP
        self._c_instruction('D', comp)      # D=comp
        self._comp_to_stack('D')            # *SP=D
        self._inc_sp()                      # ++SP

    def _compare(self, jump):           # logic operation
        self._dec_sp()                      # --SP
        self._stack_to_dest('D')            # D=*SP
        self._dec_sp()                      # --SP
        self._stack_to_dest('A')            # A=*SP
        self._c_instruction('D', 'A-D')     # D=A-D
        label_eq = self._jump('D', jump)    # D;jump to label_eq
        self._comp_to_stack('0')            # *SP=0
        label_ne = self._jump('0', 'JMP')   # 0;JMP to label_ne
        self._l_instruction(label_eq)       # (label_eq)
        self._comp_to_stack('-1')           # *SP=-1
        self._l_instruction(label_ne)       # (label_ne)
        self._inc_sp()                      # ++SP

    def _inc_sp(self):                  # increment SP
        self._a_instruction('SP')               # A=&SP
        self._c_instruction('M', 'M+1')         # SP=SP+1

    def _dec_sp(self):                  # decrement SP
        self._a_instruction('SP')               # A=&SP
        self._c_instruction('M', 'M-1')         # SP=SP-1

    def _load_sp(self):                 # load SP
        self._a_instruction('SP')               # A=&SP
        self._c_instruction('A', 'M')           # A=SP

    def _val_to_stack(self, val):       # value to stack
        self._a_instruction(val)                # A=val
        self._c_instruction('D', 'A')           # D=A
        self._comp_to_stack('D')                # *SP=D

    def _reg_to_stack(self, seg, index):    # register to stack
        self._reg_to_dest('D', self._reg_num(seg, index))   # D=R#
        self._comp_to_stack('D')                            # *SP=D

    def _mem_to_stack(self, seg, index, indir=True):    # memory to stack
        self._load_seg(seg, index, indir)       # A=seg+index
        self._c_instruction('D', 'M')           # D=*(seg+index)
        self._comp_to_stack('D')                # *SP=*(seg+index)

    def _static_to_stack(self, seg, index):     # static to stack
        self._a_instruction(self._static_name(index))   # A=&func.#
        self._c_instruction('D', 'M')                   # D=func.#
        self._comp_to_stack('D')                        # *SP=func.#

    def _comp_to_stack(self, comp):             # comp to stack
        self._load_sp()
        self._c_instruction('M', comp)          # *SP=comp

    def _stack_to_reg(self, seg, index):
        self._stack_to_dest('D')                # D=*SP
        self._comp_to_reg(self._reg_num(seg, index), 'D')

    def _stack_to_mem(self, seg, index, indir=True):    # stack to memory
        self._load_seg(seg, index, indir)
        self._comp_to_reg(R_COPY, 'D')          # R_COPY=D
        self._stack_to_dest('D')                # D=*SP
        self._reg_to_dest('A', R_COPY)          # A=R_COPY
        self._c_instruction('M', 'D')           # *(seg+index)=D

    def _stack_to_static(self, seg, index):     # stack to static
        self._stack_to_dest('D')
        self._a_instruction(self._static_name(index))
        self._c_instruction('M', 'D')

    def _stack_to_dest(self, dest):             # stack to dest
        self._load_sp()
        self._c_instruction(dest, 'M')          # dest=*SP

    def _load_sp_offset(self, offset):          # calculate SP+/-offset
        self._load_seg(self._asm_reg(R_SP), offset)

    def _load_seg(self, seg, index, indir=True):    # load address of seg+index into A and D registers
        if index == 0:
            self._load_seg_no_index(seg, indir)
        else:
            self._load_seg_index(seg, index, indir)

    def _load_seg_no_index(self, seg, indir):
        self._a_instruction(seg)                # A=seg
        if indir: self._indir(dest='AD')        # A=D=*A

    def _load_seg_index(self, seg, index, indir):
        comp = 'D+A'
        if index < 0:
            index = -index
            comp = 'A-D'
        self._a_instruction(str(index))         # A=index
        self._c_instruction('D', 'A')           # D=A
        self._a_instruction(seg)                # A=seg
        if indir: self._indir()                 # A=*seg
        self._c_instruction('AD', comp)         # A=D=seg+/-index

    def _reg_to_dest(self, dest, reg):      # register to dest
        self._a_instruction(self._asm_reg(reg)) # @R#
        self._c_instruction(dest, 'M')          # dest=R#

    def _comp_to_reg(self, reg, comp):      # comp to register
        self._a_instruction(self._asm_reg(reg)) # @R#
        self._c_instruction('M', comp)          # R#=comp

    def _reg_to_reg(self, dest, src):       # register to register
        self._reg_to_dest('D', src)
        self._comp_to_reg(dest, 'D')            # Rdest = Rsrc

    def _indir(self, dest='A'):
        self._c_instruction(dest, 'M')

    def _reg_num(self, seg, index):
        return self._reg_base(seg)+index

    def _reg_base(self, seg):
        reg_base = {'reg':R_R0, 'pointer':R_PTR, 'temp':R_TEMP}
        return reg_base[seg]

    def _static_name(self, index):
        return self._vm_file+'.'+str(index)

    def _asm_mem_seg(self, seg):        # assembler names for segments
        asm_label = {S_LCL:'LCL', S_ARG:'ARG', S_THIS:'THIS', S_THAT:'THAT'}
        return asm_label[seg]

    def _asm_reg(self, regnum):         # assembler names for registers
        return 'R'+str(regnum)

    def _jump(self, comp, jump):        # jump to a new label and return label
        label = self._new_label()
        self._a_instruction(label)              # A=label
        self._c_instruction(None, comp, jump)   # comp;jump
        return label

    def _new_label(self):               # generate a new label
        self._labelnum += 1
        return 'LABEL'+str(self._labelnum)

    def _a_instruction(self, address):  # write an assembler @ instruction
        self._out_file.write('@'+address+'\n')

    def _c_instruction(self, dest, comp, jump=None):    # write an assembler C instruction
        if dest != None:
            self._out_file.write(dest+'=')
        self._out_file.write(comp)
        if jump != None:
            self._out_file.write(';'+jump)
        self._out_file.write('\n')

    def _l_instruction(self, label):    # Write an assembler L instruction
        self._out_file.write('('+label+')\n')
