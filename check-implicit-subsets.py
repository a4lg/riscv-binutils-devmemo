#! /usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Author: Tsukasa OI <research_trasio@irq.a4lg.com>
# HEAD_LINE and TAIL_LINE:
#   Copyright (C) 2011-2022 Free Software Foundation, Inc.
# RISC-V extension implication checker:
# Usage (example):
#       ./check-implicit-subsets.py [PATH_TO_BINUTILS]
import os
import os.path
import re
import sys


# Find bfd/elfxx-riscv.c
dirs: list[str] = []
if len(sys.argv) > 1:
	dirs.append(sys.argv[1])
if 'BINUTILS_SRCDIR' in os.environ:
	dirs.append(os.environ['BINUTILS_SRCDIR'])
filename: str = None
for dir in dirs:
	fn = os.path.join(dir, 'bfd', 'elfxx-riscv.c')
	if os.path.isfile(fn):
		filename = fn
		break
if filename is None:
	print('ERROR: could not find proper source directory for bfd/elfxx-riscv.c.', file=sys.stderr)
	sys.exit(1)


# Extension implication list patterns
HEAD_LINE = 'static struct riscv_implicit_subset riscv_implicit_subsets[] ='
TAIL_LINE = '  {NULL, NULL, NULL}'
LINE_PAT = re.compile(
	'[\\s]*{[\\s]*"([^"]+)"[\\s]*,[\\s]*"([^"]+)"[\\s]*,[\\s]*(check_[a-z0-9_]*)[\\s]*}[\\s]*,')


# Make extension list and extension implication lists
exts: set[str] = set()
ext_implications: list[tuple[str, str]] = []
ext_implications_rev: dict[str, set[str]] = {}
ext_implications_fullrev: dict[str, set[str]] = {}
ext_implications_fullfwd: dict[str, set[str]] = {}
isParsing = False
with open(filename, 'r') as f:
	for ln in f:
		ln = ln.rstrip()
		if not isParsing:
			if ln != HEAD_LINE:
				continue
			isParsing = True
			f.readline()  # ignore 1 line
			continue
		if ln == TAIL_LINE:
			break
		m = LINE_PAT.match(ln)
		assert m
		parent = m.group(1)
		child = m.group(2)
		exts.add(parent)
		exts.add(child)
		ext_implications.append((parent, child))
		if parent not in ext_implications_rev:
			ext_implications_rev[parent] = set()
			ext_implications_fullrev[parent] = set()
			ext_implications_fullfwd[parent] = set()
		if child not in ext_implications_rev:
			ext_implications_rev[child] = set()
			ext_implications_fullrev[child] = set()
			ext_implications_fullfwd[child] = set()
		ext_implications_rev[child].add(parent)
		ext_implications_fullrev[child].add(parent)
		ext_implications_fullrev[child].update(ext_implications_fullrev[parent])
# Make full forward list from full reverse list
for child in exts:
	for parent in ext_implications_fullrev[child]:
		ext_implications_fullfwd[parent].add(child)


# Dump extension implications
if False:
	print('Direct Implications:')
	for ext in sorted(exts):
		print(ext + ':')
		for parent, child in ext_implications:
			if parent != ext and child != ext:
				continue
			if parent == ext:
				print('\t-> ' + child)
			else:
				print('\t<- ' + parent)
	print()
if True:
	print('Forward Implications (Full):')
	for ext in sorted(exts):
		print(ext + ':')
		for e2 in sorted(ext_implications_fullfwd[ext]):
			print('\t-> ' + e2)
	print()
if False:
	print('Reverse Implications:')
	for ext in sorted(exts):
		print(ext + ':')
		for e2 in sorted(ext_implications_rev[ext]):
			print('\t<- ' + e2)
	print()
if True:
	print('Reverse Implications (Full):')
	for ext in sorted(exts):
		print(ext + ':')
		for e2 in sorted(ext_implications_fullrev[ext]):
			print('\t<- ' + e2)
	print()


# Check
fail = False
for ext in exts:
	for sibling in ext_implications_rev[ext]:
		if not ext_implications_fullfwd[ext].issubset(ext_implications_fullfwd[sibling]):
			print('FULL CHECK NG: {}'.format(ext))
			fail = True
			break


# Exit with results
sys.exit(1 if fail else 0)
