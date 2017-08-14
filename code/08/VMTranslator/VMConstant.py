#!~/.pyenv/shims/python3
# User specific shebang line. Change to your Python interpreter dir

'''

VMConstant.py serves as a data store for VM translator constants

'''

# instruction types
C_ARITHMETIC    = 0
C_PUSH          = 1
C_POP           = 2
C_LABEL         = 3
C_GOTO          = 4
C_IF            = 5
C_FUNCTION      = 6
C_RETURN        = 7
C_CALL          = 8
C_ERROR         = 9

# segment types
S_LCL           = 'local'       # base of current VM function's local segment
S_ARG           = 'argument'    # base of current VM function's argument segment
S_THIS          = 'this'        # base of current this segment (within the heap)
S_THAT          = 'that'        # base of current that segment (within the heap)
S_PTR           = 'pointer'
S_TEMP          = 'temp'
S_CONST         = 'constant'
S_STATIC        = 'static'
S_REG           = 'reg'         # access R0-R15

# registers
R_R0 = R_SP             = 0     # stack pointer - next topmost location in the stack
R_R1 = R_LCL            = 1
R_R2 = R_ARG            = 2
R_R3 = R_THIS = R_PTR   = 3
R_R4 = R_THAT           = 4
R_R5 = R_TEMP           = 5
R_R6                    = 6
R_R7                    = 7
R_R8                    = 8
R_R9                    = 9
R_R10                   = 10
R_R11                   = 11
R_R12                   = 12
R_R13 = R_FRAME         = 13
R_R14 = R_RET           = 14
R_R15 = R_COPY          = 15
