#!/usr/bin/python

from taksutil import *

# 1 bit only
print("1 ----")
print(bin2hex("1"))

# 4 bits
print("2 ----")
print(bin2hex("10"))

# 8 bits
print("3 ----")
print(bin2hex("11000111")) # 0xc7

# 16 bits
print("4 ----")
print(bin2hex("1011111011101111"))

# 128 bits
print("5 ----")
print(bin2hex("10100101"*16))

# 32 bits cut down to 8
print("6 ----")
print(bin2hex("00000001000000100000010000001000", 9))
