from typing import List
from instruction.parser import Instruction

import sys

def read_and_parse(fname:str)->List[Instruction]:
    res = []
    buf = 0
    with open(fname, "rb") as fp:
        for idx, i in enumerate(fp.read()):
            buf |= (i << ((idx & 1) << 3)) # i << ((idx % 2) * 8)
            if idx & 1 == 1:
                res.append(Instruction(buf))
                buf = 0
    return res

def main():
    bins = read_and_parse(sys.argv[1])
    for pc, b in enumerate(bins):
        print(f"{hex(pc)[2:].zfill(4)} {b.pprint()}")
            
if __name__ == "__main__":
    main()