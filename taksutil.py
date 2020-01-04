#!/usr/bin/python3
import binascii
from random import randint

def import_from_hexstring(s):
	result = []
	temp = binascii.unhexlify(s)
	l = len(temp)
	x = [int(s[i:i+2], 16) for i in range(0,l,2)]
	result.append(x)
	x = [int(s[i:i+2], 16) for i in range(l,l*2,2)]
	result.append(x)
	return result

def export_to_hexstring(c1, put_space=True):
	result = ""
	for i in range(len(c1[0])):
		result += "%02X" % c1[0][i]
	if (put_space):
		result += " "
	for i in range(len(c1[1])):
		result += "%02X" % c1[1][i]
	return result

def key_to_hexstring(k1):
	result = ""
	for i in range(len(k1)):
		result += "%02X" % k1[i]
	return result

def gf_add(a, b):
	""" GF addition """
	return (a ^ b)

def iszero(bin_a):
	""" check if a bitstring is zero """
	return (int(bin_a, 2) == 0)

def gf_mul_mod(a, b, poly):
	""" GF mul (mod poly) """
	p = 0
	while (a and b):
		if (b & 1) != 0:
			p ^= a
		if (a & 0x80):
			a = ((a << 1) ^ 0x11B) & 0xFF
		else:
			a <<= 1
		b >>= 1
	return p;

def taks_cross_mul(c1, c2, keylen):
	result = []
	for i in range(keylen):
		t1 = gf_mul_mod(c1[0][i], c2[0][i], 0x11b);
		t2 = gf_mul_mod(c1[1][i], c2[1][i], 0x11b);
		result.append(gf_add(t1, t2))
	return result

def power(x, e, poly, bits=8):
	if (x == 0):
		return 0
	p = 1
	for i in range(bits):
		p = gf_mul_mod(p, p, poly)
		if (e & 0x80):
			p = gf_mul_mod(p, x, poly)
		e <<= 1
	return p

def make_tuple(l, i):
	return [l[0][i], l[1][i]]
"""
def tak(l1, l2, size):
	result = []
	for b in range(size):
		result.append(gf_scalar_mul(make_tuple(l1,b),make_tuple(l2,b), poly))
	return result
"""

def gf_inverse(x, poly, bits=8):
	return power(x, 0xFE, poly)

def taks_invert(ss, c1, poly, keylen):
	result = [[],[]]
	"""
	ss[i] = l[x][i] * v[x][i] + l[y][i] * v[y][i]

	conosco ss[i], l[x], l[y]
	ipotizzo un v[x] random

	ss[i] + l[x][i] * v[x][i] = l[y][i] * v[y][i]

	inverto l[y] e moltiplico

	v[y][i] = (l[y]^-1) * (ss[i] + l[x][i] * v[x][i])


	PS. funziona solo se l[y][*] != 0. Se l[y][i] = 0:

	ss[i] = l[x][i] * v[x][i] + 0

	oppure

	ss[i] = 0 + l[y][i] * v[y][i]

	Se entrambe le coordinate sono zero, niente da fare

	"""
	for i in range(keylen):
		cx = c1[0][i]
		cy = c1[1][i]
		if (cx == 0) and (cy == 0):
			vy = randint(0, 0xFF)
			vx = ss[i] ^ vy
		elif (cy == 0):
			vy = randint(0, 0xFF)
			inv = gf_inverse(cx, poly)
			vx = gf_mul_mod(inv, ss[i], poly)
		elif (cx == 0):
			vx = randint(0, 0xFF)
			inv = gf_inverse(cy, poly)
			vy = gf_mul_mod(inv, ss[i], poly)
		else:
			vx = randint(0, 0xFF)
			m = ss[i] ^ gf_mul_mod(cx, vx, poly)
			inv = gf_inverse(cy, poly)
			vy = gf_mul_mod(m, inv, poly)
		result[0].append(vx)
		result[1].append(vy)
	return result

def test(KEYLEN, num_of_tests=100):
	for test_i in range(num_of_tests):
		print("Generating LKC for node 1:")
		LKC1 = [[randint(0, 0xFF) for i in range(KEYLEN)] for c in (0, 1)]
		print(str(LKC1))
		print("Generating TV for 1 -> 2:")
		TV1to2 = [[randint(0, 0xFF) for i in range(KEYLEN)] for c in (0, 1)]
		print(str(TV1to2))
		print("Generating LKC for node 2:")
		LKC2 = [[randint(1, 0xFF) for i in range(KEYLEN)] for c in (0, 1)]
		print(str(LKC2))
		print("-"*60)
		SS1 = taks_cross_mul(LKC1, TV1to2, KEYLEN)
		print("SS1 = \x1b[92m%s\x1b[0m" % str(SS1))
		print("Calculating inverse for TKC1:")
		TKC1 = taks_invert(SS1, LKC2, 0x11B, KEYLEN)
		print("TKC1 = \x1b[93m%s\x1b[0m" % str(TKC1))
		print("Try multiplication against LKC2:")
		SS2 = taks_cross_mul(TKC1, LKC2, KEYLEN)
		print("SS2 = \x1b[91m%s\x1b[0m" % str(SS2))
		success = True
		for i in range(KEYLEN):
			if (SS1[i] != SS2[i]):
				print("i = " + str(i))
				print("LKC1[0][i]  = " + str(LKC1[0][i]))
				print("LKC1[1][i]  = " + str(LKC1[1][i]))
				print("LKC2[0][i]  = " + str(LKC2[0][i]))
				print("LKC2[1][i]  = " + str(LKC2[1][i]))
				print("TKC1[0][i]  = " + str(TKC1[0][i]))
				print("TKC1[1][i]  = " + str(TKC1[1][i]))
				print(str(SS1[i]) + " <-SS-> " + str(SS2[i]))
				success = False
				break
		if (not success):
			break
	return 0
