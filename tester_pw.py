#!/usr/bin/python3

from taksutil import *
import sys

if (len(sys.argv) < 4):
	print("Syntax: %s <lkc1> <tkc1->2> <lkc2> <tkc2->1>")
	sys.exit(-1)

# test components
lkc1 = import_from_hexstring(sys.argv[1])
tkc1 = import_from_hexstring(sys.argv[4])
lkc2 = import_from_hexstring(sys.argv[3])
tkc2 = import_from_hexstring(sys.argv[2])

tak1 = taks_cross_mul(lkc1, tkc2, 16)
tak2 = taks_cross_mul(tkc1, lkc2, 16)
print("\x1b[92m")
print(key_to_hexstring(tak1))
print(key_to_hexstring(tak2))
print("\x1b[0m")

#tak1 = taks_cross_mul(lkc2, tv2to1, 16)
#tak2 = taks_cross_mul(tkc2, lkc1, 16)
#print(str(tak1))
#print(str(tak2))
