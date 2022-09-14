#! /usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Author: Tsukasa OI <research_trasio@irq.a4lg.com>
# Note: The author assigned the copyright to FSF for GNU Binutils
#       contribution so that output of this program is considered safe
#       for GNU Binutils contribution if you assigned the copyright to
#       FSF for GNU Binutils contribution, too.
# Binutils riscv-opc.c checker
# Usage (example):
#       ./opcodes-validate-operands.py \
#               examples/opcodes-validate-operands/tokens.txt \
#               examples/opcodes-validate-operands/operands.txt
import sys

if len(sys.argv) != 3:
	print('usage: {} TOKENS OPERANDS'.format(sys.argv[0]), file=sys.stderr)
	sys.exit(1)

tokens = set()
with open(sys.argv[1], 'r') as ftoken:
	for ln in ftoken:
		tokens.add(ln.rstrip())

incomplete_tokens = set()
for t in sorted(tokens):
	if len(t) <= 1:
		continue
	while len(t) > 1:
		t = t[:-1]
		incomplete_tokens.add(t)

incomplete_tokens_permitted = set(['C', 'CF', 'F', 'O', 'V'])
incomplete_tokens_real = tokens & incomplete_tokens
assert len(incomplete_tokens_real - incomplete_tokens_permitted) == 0
tokens -= incomplete_tokens


def process_line_raw(l):
	cur = ''
	for ch in l:
		cur += ch
		if cur in incomplete_tokens:
			continue
		elif cur in tokens:
			cur = ''
			continue
		else:
			raise ValueError(cur)
	if cur != '' and (cur not in tokens):
		raise ValueError(cur)


lines = []
with open(sys.argv[2], 'r') as fi:
	for ln in fi:
		l = ln.rstrip()
		if not l:
			continue
		if l.startswith('#'):
			continue
		lines.append(l)
max_linelen = max([len(x) for x in lines])
format_str = '{{0:{}s}} : {{1}}'.format(max_linelen)
is_first = True
for l in lines:
	try:
		process_line_raw(l)
	except ValueError as f:
		if is_first:
			print(format_str.format('Operands', 'First Unrecognized Operand'))
			print('-' * (max_linelen + 30))
			is_first = False
		print(format_str.format(l, str(f)))

print('Validated finished.')
