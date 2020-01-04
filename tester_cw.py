#!/usr/bin/python3

from taksutil import *
import sys

if (len(sys.argv) < 4):
	print("Syntax: %s <lkc1> <tkc1->2> <tv1->2> <lkc2>")
	sys.exit(-1)

# test components
lkc1 = import_from_hexstring(sys.argv[1])
tkc1 = import_from_hexstring(sys.argv[2])
tv1to2 = import_from_hexstring(sys.argv[3])
lkc2 = import_from_hexstring(sys.argv[4])
#tkc2 = import_from_hexstring(sys.argv[5])
#tv2to1 = import_from_hexstring(sys.argv[6])

tak1 = taks_cross_mul(lkc1, tv1to2, 8)
tak2 = taks_cross_mul(tkc1, lkc2, 8)
print("\x1b[92m")
print(key_to_hexstring(tak1))
print(key_to_hexstring(tak2))
print("\x1b[0m")

#tak1 = taks_cross_mul(lkc2, tv2to1, 16)
#tak2 = taks_cross_mul(tkc2, lkc1, 16)
#print(str(tak1))
#print(str(tak2))
