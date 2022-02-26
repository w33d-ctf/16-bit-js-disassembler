from . import *


class Instruction:
    def split_instruction(self, instruction: int):
        opcode = (instruction & 0b0000000000001111)
        self.rd = (instruction & 0b0000000000110000) >> DESTINATION_SHIFT
        self.rs = (instruction & 0b0000000011000000) >> SOURCE_SHIFT
        self.high8 = (instruction & 0b1111111100000000) >> ADDRESS_SHIFT
        self.high10 = (instruction & 0b1111111111000000) >> LONG_ADDRESS_SHIFT

        # print(f"instruction: {hex(instruction)[2:].zfill(4)}")
        #print(f"op code:{opcode}")
        try:
            self.namedOpcode = INSTRUCTION_MAP[opcode]
            
            # jump address is retrieve from registers
            self.jumpAddress = REGISTERS[self.high8 & 0b11]
            self.jumpOffset = (instruction >> 4)
        except IndexError:
            self.namedOpcode = "DATA?"
        self.instruction = instruction

    def __init__(self, instruction: int) -> None:
        # print(f"constructor receive:{hex(instruction)}")
        self.split_instruction(instruction)

    def __str__(self) -> str:
        res = [self.namedOpcode]
        if self.namedOpcode == "CAL":
            res.append(REGISTERS[self.rd])

        elif self.namedOpcode == "LDR":
            res.append(REGISTERS[self.rd])
            res.append(REGISTERS[self.rs])
            res.append("OFF_" + hex(self.high8))
        elif self.namedOpcode == "LDA":
            res.append(REGISTERS[self.rd])
            res.append("MEM_" + hex(self.high10))

        elif self.namedOpcode == "STR":
            res.append(REGISTERS[self.rd])
            res.append(REGISTERS[self.rs])
            res.append("OFF_" + hex(self.high8))
        elif self.namedOpcode == "STA":
            res.append(REGISTERS[self.rd])
            res.append("MEM_"+hex(self.high10))
        elif self.namedOpcode == "JMR":
            res.append(REGISTERS[self.rd])
        
        elif self.namedOpcode == "MVR":
            if self.high8 == 0:
                res = [ "MOV", REGISTERS[self.rd], REGISTERS[self.rs]]
            elif (self.high8 == 0xFF) and (self.rs == self.rd):
                res = [ "DEC", REGISTERS[self.rd] ]
            else:
                res.append(REGISTERS[self.rd])
                res.append(REGISTERS[self.rs])
                res.append("OFF_"+hex(self.high8))
        elif self.namedOpcode == "MVV":
            if self.high10 & 3 == 0:
                res = ["MVI", REGISTERS[self.rd], hex(self.high8)]
            elif self.high10 & 3 == 1:
                res = ["ADI", REGISTERS[self.rd], hex((self.high8 << 24) >> 24)]
            elif self.high10 & 3 == 2:
                res = ["MUI", REGISTERS[self.rd], hex(self.high8)]
            elif self.high10 & 3 == 3:
                res = ["AUI", REGISTERS[self.rd], hex(self.high8)]
            
            if (res[0] in [ "AUI", "ADI" ]) and (res[2] == hex(0)):
                res = ["NOP"]
        elif self.namedOpcode == "PSH":
            res.append(REGISTERS[self.rs])
        elif self.namedOpcode == "POP":
            res.append(REGISTERS[self.rd])
        elif self.namedOpcode == "NOA":
            noa_op = (self.instruction & 0xF0) >> 4
            try:
                res = [ NOA[noa_op] ]
            except IndexError:
                res = [ "DATA?" ]
        elif self.namedOpcode == "JCP":
            res = [ "J"+JUMP[self.high8 >> 2] , REGISTERS[self.rd], REGISTERS[self.rs], self.jumpAddress]
        elif self.namedOpcode == "ATH":
            resultMode = (self.high8 & 0b00010000) >> 4

            arithmeticOperation = (self.high8 & 0b00001111)
            shiftAmount = (self.high8 & 0b11100000) >> 5
            resultRegister = REGISTERS[self.rd] if (resultMode == DESTINATION_MODE) else REGISTERS[self.rs]

            if self.namedOpcode in [ "INC", "DEC", "LSF", "RSF" ,"NOT" ]:
                if self.namedOpcode in [ "INC", "DEC" ]:
                    res = [ self.namedOpcode, REGISTERS[self.rd] ]
                elif self.namedOpcode in [ "LSF", "RSF" ]:
                    res = [ self.namedOpcode, REGISTERS[self.rd], hex(shiftAmount) ]
                else: # NOT
                    res = [ self.namedOpcode, REGISTERS[self.rs] ]
            else:
                res = [ ARITHMETIC[arithmeticOperation], REGISTERS[self.rd], REGISTERS[self.rs]]
        else:
            res.append("TBD")
        return " ".join(res)
    def pprint(self)->str:
        return "{:<20} {}".format(str(self), hex(self.instruction)[2:].zfill(4))