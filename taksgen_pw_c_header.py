#!/usr/bin/python3

# -*- coding: utf-8 -*-

from random import randint
from taksutil import *

poly = 0b100011011 # rijndael poly
KEYLEN = (128)/8

syntax_help = "\x1b[91m"+\
	"┏━━━━━━━━━━━ Fast TAKS key generator ━━━━━━━━┓\n"+\
	"┣▶author: Walter Tiberti                     ┃\n"+\
	"┣▶email: walter.tiberti@graduate.univaq.it   ┃\n"+\
	"┃                                            ┃\n"+\
	"┣▶syntax:<cmd> <keybits> <poly HEX> <nodes#> ┃\n"+\
	"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"+"\x1b[0m"

title = "\x1b[92m"+\
	"┏━━━━━━━━━━━ Fast TAKS key generator ━━━━━━━━┓\n"+\
	"┣▶author: Walter Tiberti                     ┃\n"+\
	"┣▶email: walter.tiberti@graduate.univaq.it   ┃\n"+\
	"┃                                            ┃\n"+\
	"┣▶keylen (bytes): %27d┃\n"+\
	"┣▶poly:  %#36x┃\n"+\
	"┣▶keys #: %35d┃\n"+\
	"┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"+"\x1b[0m"

lkc_done = "#define LKC_%d \"%s\""
tkc_done = "#define TKC_%d_%d \"%s\""
title_ss = "\x1b[94m┣━▶ TAK for %d ▬▶ %d"+"\x1b[0m"

def main(args):
	#test(32, 100000)
	try:
		keylen = int(args[1]) // 8
		poly = int(args[2], 16)
		node_number = int(args[3])
	except:
		print(syntax_help)
		sys.exit(-1)
	pass
	print(title % (keylen, poly, node_number))

	nodes = {}
	"""
	LKC
	"""
	for n in range(node_number):
		nodes[n] = {}
		lkc = nodes[n]["lkc"] = random_component(keylen)
		nodes[n]["tkc"] = {}
		for i in range(node_number):
			nodes[n]["tkc"][i] = {}
		print(lkc_done % (n, export_to_hexstring(lkc, False)))
	"""
	TKC
	"""
	for i in range(node_number-1):
		for j in range(i+1, node_number):
			random_tak = [randint(0, 0xFF) for i in range(keylen)]

			# tkc[j->i]
			tjx = [randint(0, 0xFF) for i in range(keylen)]
			tjy = []
			for e in range(len(tjx)):
				lix = nodes[i]["lkc"][0]
				liy = nodes[i]["lkc"][1]
				k = gf_add(random_tak[e], gf_mul_mod(liy[e], tjx[e], poly))
				inv_lx = gf_inverse(lix[e], poly)
				tjy.append(gf_mul_mod(k, inv_lx, poly))
			tkcj = [tjy, tjx]
			nodes[i]["tkc"][j] = []
			nodes[i]["tkc"][j].append(tjy)
			nodes[i]["tkc"][j].append(tjx)
			print(tkc_done % (i,j,export_to_hexstring(tkcj, False)))

			# tkc[j->i]
			tix = [randint(0, 0xFF) for i in range(keylen)]
			tiy = []
			for e in range(len(tix)):
				ljx = nodes[j]["lkc"][0]
				ljy = nodes[j]["lkc"][1]
				k = gf_add(random_tak[e], gf_mul_mod(ljy[e], tix[e], poly))
				inv_lx = gf_inverse(ljx[e], poly)
				tiy.append(gf_mul_mod(k, inv_lx, poly))
			tkci = [tiy, tix]
			nodes[j]["tkc"][i] = []
			nodes[j]["tkc"][i].append(tiy)
			nodes[j]["tkc"][i].append(tix)
			print(tkc_done % (j,i,export_to_hexstring(tkci, False)))
	"""
	Test (inserted as C-style comment
	"""
	print("/*")
	for i in range(node_number-1):
		for j in range(i+1, node_number):
			l = nodes[i]["lkc"]
			t = nodes[i]["tkc"][j]
			ss1 = taks_cross_mul(l, t, keylen)
			print(title_ss % (i, j))
			print(key_to_hexstring(ss1))

			l = nodes[j]["lkc"]
			t = nodes[j]["tkc"][i]
			ss2 = taks_cross_mul(l, t, keylen)
			print(title_ss % (j, i))
			print(key_to_hexstring(ss2))
	print("*/")
	return 0


def random_component(size):
	return [[randint(0, 0xFF) for i in range(size)] for c in (0, 1)]


if __name__ == "__main__":
	import sys
	main(sys.argv)
