MAX_INT = 0xFFFF
MEM_SIZE = 0xFFFF
STACK_SIZE = 0xFF
REGISTERS = ['A', 'B', 'C', 'D']
INSTRUCTION_MAP = [
    'MVR',
    'MVV',
    'LDR',
    'STA',
    'ATH',
    'CAL',
    'JCP',
    'PSH',
    'POP',
    'JMP',
    'JMR',
    'LDA',
    'STR',
    'NOA'
]

DESTINATION_SHIFT = 4
SOURCE_SHIFT = 6
LONG_ADDRESS_SHIFT = 6
ADDRESS_SHIFT = 8
OFFSET_SHIFT = 8
OPERATION_SHIFT = 8,
ARITHMETIC_MODE_SHIFT = 12
BITWISE_SHIFT_SHIFT = 13

NOA = [
    "NOP",
    "RET",
    "SYS",
    "HLT"
]

JUMP = {
    0:"EQ", 
    1:"NEQ",
    2:"LT", 
    3:"GT", 
    4:"LTE",
    5:"GTE",
    6:"ZER",
    7:"NZE",
# WARN: i haven't figure out what these mean below, please use them carefully 
# 4:"R1", 
# 6:"R2", 
# 8:"AR",
# 10:"OP",
}

ARITHMETIC = {
0:"ADD",
1:"SUB",
2:"MUL",
3:"DIV",
4:"INC",
5:"DEC",
6:"LSF",
7:"RSF",
8:"AND",
9:"OR",
10:"XOR",
11:"NOT",
# see ATH parse for these marcos 
# 0:"DESTINATION_MODE",
# 1:"SOURCE_MODE",
}
DESTINATION_MODE = 0
SOURCE_MODE = 1


OS = {
    "STDOUT": 0,
    "STDIN": 1
},

DIRECT_ASSIGNMENT = 0
BUFFER_ASSIGNMENT = 1
STRING_ASSIGNMENT = 2

DEBUG = { "NUM_PAGES": 255 }
