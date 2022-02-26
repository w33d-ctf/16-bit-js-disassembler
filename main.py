from instruction.parser import Instruction

import sys

with open(sys.argv[1], 'rb') as f:
    inc = 0
    while True:
        instruction = f.read(2)
        if instruction == "":
            break
        try:
            print("{:04x}\t{:04x}\t\t{}".format(inc, int.from_bytes(instruction, byteorder='little'), Instruction(
                int.from_bytes(instruction, byteorder='little'))))
        except IndexError:
            pass
            #print("{:02x} {}".format(inc, instruction))
        inc += 2
