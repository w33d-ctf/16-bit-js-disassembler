# 16-bit-js-disassembler
a simple disassembler to solve chall of TSJ-CTF javascript VM

## in main loop
* 0x11e: global loop ctr
* 0x11f: encode times?

## in reader loop
* 0x11b: len of str
* 0x11c: loop ctr
* 0x155: start address of store input

## enc_0x9c
* 0x11d: local loop ctr
* loop for 52 times
* do substitution

## enc_0xd3
* 0x11d: local loop ctr
* loop for 52 times
* do key addition

## final checker loop 0x1b
* 0x11d: local loop ctr
* compare encdoe string from 0x1bf
