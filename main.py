from instruction.parser import Instruction

import sys

with open(sys.argv[1], 'rb') as f:
    inc = 0
    while True:
        instruction = f.read(2)
        if instruction == "":
            break
        try:
            print("{:02x} {}".format(inc, Instruction(
                int.from_bytes(instruction, byteorder='little'))))
        except IndexError:
            print("{:02x} {}".format(inc, instruction))
        inc += 2
print(Instruction(0b0000111100001011))