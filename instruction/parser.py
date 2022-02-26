from . import *

class Instruction:
    def split_instruction(self, instruction:int):
        opcode = (instruction & 0b0000000000001111)
        self.rd = (instruction & 0b0000000000110000) >> DESTINATION_SHIFT
        self.rs = (instruction & 0b0000000011000000) >> SOURCE_SHIFT
        self.high8 = (instruction & 0b1111111100000000) >> ADDRESS_SHIFT
        self.high10 = (instruction & 0b1111111111000000) >> LONG_ADDRESS_SHIFT

        print(f"op code:{opcode}")
        self.namedOpcode = INSTRUCTION_MAP[opcode]
        # TODO: find out jump address
        # self.jumpAddress = registers[REGISTERS[self.high8 & 0b11]]
        self.jumpOffset = (instruction >> 4)

    def __init__(self, instruction:int) -> None:
        self.split_instruction(instruction)
    
    def __str__(self) -> str:
        res = [ self.namedOpcode ]
        if self.namedOpcode == "CAL":
            res.append("REG_"+str(REGISTERS[self.rd]))
        
        elif self.namedOpcode == "LDR":
            res.append(REGISTERS[self.rd])
            res.append(REGISTERS[self.rs])
            res.append("OFF_"+hex(self.high8))
        elif self.namedOpcode == "LDA":
            res.append(REGISTERS[self.rd])
            res.append("MEM_"+hex(self.high10))

        elif self.namedOpcode == "STR":
            res.append(REGISTERS[self.rd])
            res.append(REGISTERS[self.rs])
            res.append("OFF_"+hex(self.high8))
        elif self.namedOpcode == "STA":
            res.append(REGISTERS[self.rd])
            res.append("MEM_"+hex(self.high10))
        else:
            res.append("TBD")
        return " ".join(res)