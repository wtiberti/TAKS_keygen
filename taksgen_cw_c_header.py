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
tv_done = "#define TV_%d_%d \"%s\""
tkc_done = "#define TKC_%d_%d \"%s\""

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
		print(lkc_done % (n, export_to_hexstring(lkc, False)))

	"""
	TV
	"""
	for i in range(node_number):
		all_but_i = list(range(node_number))
		all_but_i.remove(i)
		nodes[i]["tv"] = {}
		for j in all_but_i:
			tv = nodes[i]["tv"][j] = random_component(keylen)
			print(tv_done % (i,j,export_to_hexstring(tv, False)))
	"""
	TAK
	"""
	for i in range(node_number):
		all_but_i = list(range(node_number))
		all_but_i.remove(i)
		nodes[i]["ss"] = {}
		for j in all_but_i:
			l = nodes[i]["lkc"]
			t = nodes[i]["tv"][j]
			ss = nodes[i]["ss"][j] = taks_cross_mul(l, t, keylen)
	"""
	TKC
	"""
	for i in range(node_number):
		# Per ogni nodo, recurepero la lista di tutti gli altri nodi
		all_but_i = list(range(node_number))
		all_but_i.remove(i)
		nodes[i]["tkc"] = {}
		for j in all_but_i:
			tkc = nodes[i]["tkc"][j] = taks_invert(nodes[i]["ss"][j], nodes[j]["lkc"], poly, keylen)
			print(tkc_done % (i,j,export_to_hexstring(tkc, False)))
	return 0


def random_component(size):
	return [[randint(0, 0xFF) for i in range(size)] for c in (0, 1)]


if __name__ == "__main__":
	import sys
	main(sys.argv)
