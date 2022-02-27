from typing import List


def get_mem()->List[int]:
    res = []
    buf = 0
    with open("../chall.bin", "rb") as fp:
        for idx, i in enumerate(fp.read()):
            buf |= (i << ((idx & 1) << 3)) # i << ((idx % 2) * 8)
            if idx & 1 == 1:
                # print(f"parsing {idx >> 1}")
                res.append(buf)
                buf = 0
    return res

gctr = 0
input_off = 0x155

def dec_0x9c(MEM:List[int]):
    for i in range(51, -1, -1):
        a = MEM[input_off + MEM[0x120 + i]]
        b = MEM[input_off + i]
        MEM[input_off + MEM[0x120 + i]] = b
        MEM[input_off + i] = a

def dec_0xd3(MEM:List[int]):
    global gctr
    for i in range(51, -1, -1):
        MEM[input_off + i] -= (MEM[0x18a + (i + gctr + 0xb) % 52 ])
        MEM[input_off + i] %= 256

def main():
    global gctr
    mem  = get_mem()
    # print(mem)
    gctr = mem[0x11f] - 1
    mem = mem[:0x155] + mem[0x1bf:0x1bf+52] + mem[0x155+52:]

    print(bytes(mem[0x155:0x155+52]))

    while gctr >= 0:
        print(gctr)
        dec_0xd3(mem)
        dec_0x9c(mem)
        gctr -= 1
    print(bytes(mem[0x155:0x155+52]))
main()