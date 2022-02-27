from typing import List
from instruction import REGISTERS
from instruction.parser import Instruction

import sys

def read_and_parse(fname:str)->List[Instruction]:
    res = []
    buf = 0
    with open(fname, "rb") as fp:
        for idx, i in enumerate(fp.read()):
            buf |= (i << ((idx & 1) << 3)) # i << ((idx % 2) * 8)
            if idx & 1 == 1:
                # print(f"parsing {idx >> 1}")
                res.append(Instruction(buf))
                buf = 0
    return res

def main():
    bins = read_and_parse(sys.argv[1])
    # print("done reading bins, start printing")
    
    labels = []
    for l in open("labels.txt", "r").read().splitlines():
        labels.append(int(l.strip(), 16))
    # prevent you write duplicated address
    labels = list(set(labels))
    
    code_folding = []
    comments = {}
    # mem read/write recognization
    ## read
    ldr_pos = [
        idx
        for idx, ins in enumerate(bins)
        if str(ins)[:3] == "LDR" and str(ins)[-7:] == "OFF_0x0"
    ]
    for pos in ldr_pos:
        ldr_addr = pos
        # for example
        # 0052 MVI A 0x1b           1b01
        # 0053 AUI A 0x1            01c1
        # 0054 LDR A A OFF_0x0      0002;  mov A, MEM[0x11b]
        AUI_loc = -1
        MVI_loc = -1
        while pos > 0:
            pos -= 1
            if str(bins[pos]) == "NOP":
                continue
            elif str(bins[pos])[:3] in [ "AUI", "MVI" ]:
                if str(bins[pos])[:3] == "AUI":
                    if AUI_loc != -1:
                        break
                    if bins[ldr_addr].rs != bins[pos].rd:
                        break
                    AUI_loc = pos
                else:
                    if MVI_loc != -1:
                        break
                    if bins[ldr_addr].rs != bins[pos].rd:
                        break
                    MVI_loc = pos
                    break
            else:
                #print(f"detected wrong inst {bins[pos]}")
                break
        #print(f"pos {ldr_addr} AUI:{AUI_loc} MVI:{MVI_loc}")
        if AUI_loc != -1 and MVI_loc != -1:
            code_folding.append((MVI_loc, ldr_addr))
            comments.update(
                {
                    ldr_addr:
                    f"{REGISTERS[bins[ldr_addr].rd]} = " + \
                    f"MEM[{hex(bins[MVI_loc].high8 + (bins[AUI_loc].high8 << 8))}]"
                }
            )
    ## write
    str_pos = [
        idx
        for idx, ins in enumerate(bins)
        if str(ins)[:3] == "STR" and str(ins)[-7:] == "OFF_0x0"
    ]
    for pos in str_pos:
        str_addr = pos
        # for example
        # 0091 MVI B 0x1c           1c11
        # 0092 AUI B 0x1            01d1
        # 0093 STR B A OFF_0x0      001c;  MEM[0x11c] = A
        AUI_loc = -1
        MVI_loc = -1
        while pos > 0:
            pos -= 1
            if str(bins[pos]) == "NOP":
                continue
            elif str(bins[pos])[:3] in [ "AUI", "MVI" ]:
                if str(bins[pos])[:3] == "AUI":
                    if AUI_loc != -1:
                        break
                    if bins[str_addr].rd != bins[pos].rd:
                        break
                    AUI_loc = pos
                else:
                    if MVI_loc != -1:
                        break
                    if bins[str_addr].rd != bins[pos].rd:
                        break
                    MVI_loc = pos
                    break
            else:
                #print(f"detected wrong inst {bins[pos]}")
                break
        #print(f"pos {ldr_addr} AUI:{AUI_loc} MVI:{MVI_loc}")
        if AUI_loc != -1 and MVI_loc != -1:
            code_folding.append((MVI_loc, str_addr))
            comments.update(
                {
                    str_addr:
                    f"MEM[{hex(bins[MVI_loc].high8 + (bins[AUI_loc].high8 << 8))}] = " + \
                    f"{REGISTERS[bins[str_addr].rs]}"
                }
            )
    
    # mov 16 imm bit
    mvi_pos = [
        idx
        for idx, ins in enumerate(bins)
        if str(ins)[:3] == "MVI"
    ]
    for pos in mvi_pos:
        if pos + 1 >= len(bins):
            break
        mvi_addr = pos
        while pos < len(bins):
            pos += 1
            if str(bins[pos]) == "NOP":
                continue
            
            if str(bins[pos])[:3] == "AUI" and bins[pos].rd == bins[mvi_addr].rd:
                for st, ed in code_folding:
                    if st <= mvi_addr and pos <= ed:
                        break    
                else:
                    code_folding.append((mvi_addr, pos))
                    comments.update({
                        pos:f"{REGISTERS[bins[pos].rd]} = {hex(bins[mvi_addr].high8 + (bins[pos].high8 << 8))}"
                    })
            break
    
    
    for l in open("comments.txt").read().splitlines():
        tar_pc, comment = l.split(";")
        pc = int(tar_pc, 16)
        if pc not in comments:
            comments.update({pc:comment})
        else:
            comments[pc] = "{:<20}     ;{}".format(comments[pc], comment)
    code_folding = sorted(code_folding, key=lambda x:x[0])

    pc = 0
    #print(code_folding)
    while pc < len(bins):
        b = bins[pc]

        if pc in labels:
            print(f"LAB_{hex(pc)[2:].zfill(4)}:")
        if code_folding != []:
            if code_folding[0][0] == pc:
                for i in range(code_folding[0][0], code_folding[0][1]+1):
                    if i != code_folding[0][1] and i not in comments:
                        print(f"{hex(pc)[2:].zfill(4)}")
                    else:
                        print(f"{hex(pc)[2:].zfill(4)} {comments[i]}")
                    pc += 1
                code_folding = code_folding[1:]
                continue
        # print(f"printing at pc:{hex(pc)[2:].zfill(4)}")
        out = f"{hex(pc)[2:].zfill(4)} {b.pprint()}"
        if pc in comments:
            out += f";{comments[pc]}"
        print(out)
        pc += 1    
if __name__ == "__main__":
    main()