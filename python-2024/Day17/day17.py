#!/usr/bin/env python3

from collections import defaultdict, Counter
from functools import lru_cache
import ast
import collections
import hashlib
import itertools
import math
import string
import sys
import timeit
import unittest
import utils.const as const
import utils.data as data
#import utils.direction as direc
import utils.frac as frac
import utils.graph as graph
import utils.grid as grid
import utils.lines as lines
import utils.ocr as ocr
import utils.ranges as ranges
import utils.input as readin
pr = print

class Tests(unittest.TestCase):
	def setUp(self):
		self.testinput = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
		self.test = parse_input(self.testinput.split("\n"))

		self.testinput2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
		self.test2 = parse_input(self.testinput2.split("\n"), p2mode = True)
	
	def test_part1(self):
		self.assertEqual(part1(self.test), "4,6,3,5,6,3,5,2,1,0")
		pass
		
	def test_part2(self):
		self.assertEqual(part2(self.test2), 117440)
		pass

def parse_input(inp, p2mode = False):
	regs = []
	past_regs = False
	for idx, line in enumerate(inp):
		if past_regs:
			return regs, list(int(c) for c in line.strip().split()[1].split(","))
		elif len(line.strip()) == 0:
			past_regs = True
		else:
			regs.append(int(line.strip().split()[-1]))

	return readin.int_single_input(inp) #123
	return readin.int_list_single_space_separated_input(inp) #123 456
	return readin.int_list_single_comma_separated_input(inp) #123,456
	return readin.int_list_single_arbitrary_separated_input(inp, "x") #123x456

	return readin.int_list_multiple_input(inp) # 123\n456
	return readin.int_list_multiple_space_separated_input(inp) # 123 456\n789 012
	return readin.int_list_multiple_arbitrary_separated_input(inp, "x") # 123x456\n789x012

	return readin.string_single_input(inp) #string
	return readin.string_list_input(inp) # string\ntext

	return readin.grid_input(inp)
	return readin.grid_set_input(inp, "#")
	
	return readin.int_string_input(inp) #123456 -> [1, 2, 3, 4, 5, 6]
	return readin.int_list_input(inp) # 123\n456
	return readin.chars_input(inp) #ABC -> [A, B, C]

def part1(inp):
	#pr(inp)
	regs, prog = inp
	ip = 0
	out = []
	while ip < len(prog):
		ci = prog[ip]
		operand = prog[ip + 1]
		if ci == 0: # adv
			num = regs[0]
			denom = 2 ** get_operand(regs, operand)
			regs[0] = num // denom
		elif ci == 1: # bxl
			regs[1] = regs[1] ^ operand
		elif ci == 2: # bst
			regs[1] = get_operand(regs, operand) % 8
		elif ci == 3: # jnz
			if regs[0] != 0:
				ip = operand
				continue
		elif ci == 4: # bxc
			regs[1] = regs[1] ^ regs[2]
		elif ci == 5: # out
			out.append(get_operand(regs, operand) % 8)
		elif ci == 6: # bdv
			num = regs[0]
			denom = 2 ** get_operand(regs, operand)
			regs[1] = num // denom
		elif ci == 7: # cdv
			num = regs[0]
			denom = 2 ** get_operand(regs, operand)
			regs[2] = num // denom
		else:
			assert False


		ip += 2
	o = ""
	for o2 in out:
		o += str(o2)
		o += ","
	return o[:-1]

def get_operand(regs, op):
	if op in (0, 1, 2, 3):
		return op
	elif op in (4, 5, 6):
		return regs[op - 4]
	elif op == 7:
		assert False

def part2(inp):
	regs, prog = inp
	cur_as = [0]
	xor1 = prog[3]
	xor2 = prog[7]
	for v in reversed(prog):
		target = v
		ncas = []
		for ca in cur_as:
			rmin = max(1, ca * 8)
			rmax = ca * 8 + 7
			r = range(rmin, rmax + 1)
			valid = None
			for possible in r:
				rb = possible % 8
				rc = possible // (2 ** (rb ^ 3))
				if (target ^ rc ^ xor1 ^ xor2) % 8 == possible % 8:
					ncas.append((ca * 8) + rb)
		cur_as = ncas
	return min(cur_as)

def sim(ra):
	o = []
	while ra > 0:
		rb = ra % 8
		rb ^= 3
		rc = ra // (2 ** rb)
		rb ^= 5
		ra //= 8
		rb ^= rc
		o.append(rb % 8)
	return tuple(o)

def main():
	t0 = timeit.default_timer()
	with open(sys.argv[1], "r") as f:
		i = parse_input(f.readlines())
	print(part1(i))
	t1 = timeit.default_timer()
	with open(sys.argv[1], "r") as f:
		i = parse_input(f.readlines(), True)
	print(part2(i))
	t2 = timeit.default_timer()
	if len(sys.argv) > 2:
		print(f"Part 1: {t1 - t0} seconds")
		print(f"Part 2: {t2 - t1} seconds")

if __name__ == '__main__':
	if len(sys.argv) < 2:
		unittest.main()
	else:
		main()
