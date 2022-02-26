from typing import List
from instruction import *
from instruction.parser import Instruction

MX_LOOK_BACK = 4
labels = [0] # entry point
code_sect = set()
v_pc = 0 # program counter

def jump_anal(codes:List[Instruction])->int:
    pass

# since its outputs possibly are sh!ts
def label_n_flow_anal(codes:List[Instruction])->List[int]:
    global labels
    global v_pc
    global code_sect
    v_stack = []

    while True:
        if v_pc not in v_pc not in code_sect:
            code_sect.add(v_pc)
            if codes[v_pc].namedOpcode[0] == "J":
                try:
                    j_addr = jump_anal(codes)
                    labels.append()
                except:
                    pass
        elif len(v_stack) != 0:
            pass
        else:
            break
    return labels