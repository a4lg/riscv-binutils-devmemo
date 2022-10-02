#! /usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Author: Tsukasa OI <research_trasio@irq.a4lg.com>
# Binutils opcode constant ChangeLog generator
# Usage (example):
#       cat examples/add-opcode-const-mklog/zpn-zpsfoperand.txt | ./add-opcode-const-mklog.py

import re
import sys

POS_LIMIT = 74
POS_TAB = 8

PAT_RAW    = re.compile('[0-9A-Za-z_]+')
PAT_DEFINE = re.compile('#define[\\s]+([0-9A-Za-z_]+)([\\s]+.*)?')

START_LINE = '('
#START_LINE = '* opcode/riscv-opc.h ('

out_line = '\t' + START_LINE
out_col = POS_TAB + len(START_LINE)
is_start = True

for ln in sys.stdin:
	ln = ln.rstrip()
	s = None
	m = PAT_RAW.fullmatch(ln)
	if m:
		s = ln
	if not s:
		m = PAT_DEFINE.fullmatch(ln)
		if m:
			s = m.group(1)
	if not s:
		continue
	if out_col + len(s) + (0 if is_start else 1) + 1 > POS_LIMIT:
		print(out_line)
		out_line = '\t'
		out_col = POS_TAB
		is_start = True
	if not is_start:
		out_line += ' '
		out_col += 1
	out_line += s
	out_col += len(s)
	out_line += ','
	out_col += 1
	is_start = False
print(out_line[:-1] + '): ')
