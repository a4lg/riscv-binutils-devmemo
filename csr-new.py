#! /usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Author: Tsukasa OI <research_trasio@irq.a4lg.com>
# Note: The author assigned the copyright to FSF for GNU Binutils
#       contribution so that output of this program is considered safe
#       for GNU Binutils contribution if you assigned the copyright to
#       FSF for GNU Binutils contribution, too.
# Binutils new CSR template generator
# Usage (example):
#       cat examples/csr-new/smstateen.txt | ./csr-new.py

import math
import os
import os.path
import re
import shutil
import sys

PAT_CSR_NAME = re.compile('[a-z0-9]+')
PAT_CSR_CLASS = re.compile('CSR_CLASS_[A-Z0-9_]+')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'out/csr-new')
if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)

DEFAULT_CSR_MIN_VERSION = 'none'
DEFAULT_CSR_CLASS       = 'CSR_CLASS_I'

CSR_CLASSES_I = frozenset([
	'CSR_CLASS_I',
	'CSR_CLASS_I_32',
])

CSR_CLASSES_RV32 = frozenset([
	'CSR_CLASS_I_32',
	'CSR_CLASS_H_32',
	'CSR_CLASS_SMSTATEEN_32',
	'CSR_CLASS_SMSTATEEN_AND_H_32',
	'CSR_CLASS_SSCOFPMF_32',
	'CSR_CLASS_SSTC_32',
	'CSR_CLASS_SSTC_AND_H_32',
])

CSR_CLASSES_H = frozenset([
	# Exclude CSR_CLASS_H*
	'CSR_CLASS_SMSTATEEN_AND_H',
	'CSR_CLASS_SMSTATEEN_AND_H_32',
	'CSR_CLASS_SSTC_AND_H',
	'CSR_CLASS_SSTC_AND_H_32',
])

CSR_EXTENSIONS = {
	'CSR_CLASS_I':    "`i'",
	'CSR_CLASS_I_32': "`i'",
	'CSR_CLASS_H':    "`h'",
	'CSR_CLASS_H_32': "`h'",
	'CSR_CLASS_F':    "`f'",
	'CSR_CLASS_ZKR':  "`zkr'",
	'CSR_CLASS_V':    "`v'",
	'CSR_CLASS_SMSTATEEN':          "`smstateen'",
	'CSR_CLASS_SMSTATEEN_AND_H':    "`smstateen'",
	'CSR_CLASS_SMSTATEEN_32':       "`smstateen'",
	'CSR_CLASS_SMSTATEEN_AND_H_32': "`smstateen'",
	'CSR_CLASS_SSCOFPMF':    "`sscofpmf'",
	'CSR_CLASS_SSCOFPMF_32': "`sscofpmf'",
	'CSR_CLASS_SSTC':          "`sstc'",
	'CSR_CLASS_SSTC_AND_H':    "`sstc'",
	'CSR_CLASS_SSTC_32':       "`sstc'",
	'CSR_CLASS_SSTC_AND_H_32': "`sstc'",
}

PRIV_VERSIONS = {
	'none':  (0, 'PRIV_SPEC_CLASS_NONE', None),
	'1.9.1': (1, 'PRIV_SPEC_CLASS_1P9P1', '1p9p1'),
	'1.10':  (2, 'PRIV_SPEC_CLASS_1P10', '1p10'),
	'1.11':  (3, 'PRIV_SPEC_CLASS_1P11', '1p11'),
	'1.12':  (4, 'PRIV_SPEC_CLASS_1P12', '1p12'),
	'draft': (math.inf, 'PRIV_SPEC_CLASS_DRAFT', None),
}
CSR_VERSION_CONSTANTS_REV = dict((v[1], k) for k, v in PRIV_VERSIONS.items())
assert(DEFAULT_CSR_MIN_VERSION in PRIV_VERSIONS)

if sys.stdin.isatty():
	print('Type CSR_NAME CSR_VALUE [MIN_VERSION] [CSR_CLASS] lines below:', file=sys.stderr)
for ln in sys.stdin:
	ln = ln.rstrip()
	if ln.startswith('!!!!'):
		shutil.rmtree(DATA_DIR)
		os.makedirs(DATA_DIR)
		continue
	if not ln or ln.startswith('#'):
		cmt_c = ''
		cmt_s = ''
		cmt_d = '# Delete this line before copying'
		label = ln[1:].strip() if ln else ''
		if label:
			cmt_c = '/* {} */'.format(label)
			cmt_s = '# {}'.format(label)
			cmt_d = '# {} (delete this line before copying)'.format(label)
		with open(os.path.join(DATA_DIR, 'riscv-opc.1.h'), 'a') as f:
			print(cmt_c, file=f)
		with open(os.path.join(DATA_DIR, 'riscv-opc.2.h'), 'a') as f:
			print(cmt_c, file=f)
		with open(os.path.join(DATA_DIR, 'csr-dw-regnums.s'), 'a') as f:
			print('\t' + cmt_s, file=f)
		with open(os.path.join(DATA_DIR, 'csr-dw-regnums.d'), 'a') as f:
			print('  ' + cmt_d, file=f)
		with open(os.path.join(DATA_DIR, 'csr.s'), 'a') as f:
			print('\t' + cmt_s, file=f)
		for k, (nver_k, cclass_k, vprefix) in PRIV_VERSIONS.items():
			if vprefix is None:
				continue
			with open(os.path.join(DATA_DIR, 'csr-version-{}.d'.format(vprefix)), 'a') as f:
				print(cmt_d, file=f)
			with open(os.path.join(DATA_DIR, 'csr-version-{}.l'.format(vprefix)), 'a') as f:
				print(cmt_d, file=f)
		continue
	#
	#   Tokenize and Parse
	#
	tokens = ln.split()
	assert(len(tokens) >= 2 and len(tokens) <= 4)
	if len(tokens) < 3:
		tokens.append(DEFAULT_CSR_MIN_VERSION)
	if len(tokens) < 4:
		tokens.append(DEFAULT_CSR_CLASS)
	if tokens[2] in CSR_VERSION_CONSTANTS_REV:
		tokens[2] = CSR_VERSION_CONSTANTS_REV[tokens[2]]
	name   = tokens[0]
	value  = int(tokens[1], 0)
	minver = tokens[2]
	cclass = tokens[3]
	is_rdonly = (value & 0xc00) == 0xc00
	assert(PAT_CSR_NAME.fullmatch(name))
	assert(value >= 0 and value < 0x1000)
	assert(minver in PRIV_VERSIONS)
	assert(PAT_CSR_CLASS.fullmatch(cclass))
	nver = PRIV_VERSIONS[minver][0]
	#
	#   Write to corresponding files
	#
	with open(os.path.join(DATA_DIR, 'riscv-opc.1.h'), 'a') as f:
		print('#define CSR_{0} 0x{1:x}'.format(name.upper(), value), file=f)
	with open(os.path.join(DATA_DIR, 'riscv-opc.2.h'), 'a') as f:
		print('DECLARE_CSR({0}, CSR_{1}, {2}, {3}, PRIV_SPEC_CLASS_{4})'.format(
			name, name.upper(), cclass, PRIV_VERSIONS[minver][1],
			'NONE' if nver == 0 else 'DRAFT'), file=f)
	with open(os.path.join(DATA_DIR, 'csr-dw-regnums.s'), 'a') as f:
		print('\t.cfi_offset {0}, {1:d}'.format(name, value*4), file=f)
	with open(os.path.join(DATA_DIR, 'csr-dw-regnums.d'), 'a') as f:
		print('  DW_CFA_offset_extended_sf: r{1:d} \({0}\) at cfa\+{2:d}'.format(name, value+4096, value*4), file=f)
	with open(os.path.join(DATA_DIR, 'csr.s'), 'a') as f:
		print('\tcsr {}'.format(name), file=f)
	for k, (nver_k, cclass_k, vprefix) in PRIV_VERSIONS.items():
		if vprefix is None:
			continue
		with open(os.path.join(DATA_DIR, 'csr-version-{}.d'.format(vprefix)), 'a') as f:
			print(('[ \t]+[0-9a-f]+:[ \t]+{0:03x}02573[ \t]+csrr[ \t]+a0,{1}\n' +
				'[ \t]+[0-9a-f]+:[ \t]+{0:03x}59073[ \t]+csrw[ \t]+{1},a1').format(value,
				name if nver_k >= nver else '0x{:x}'.format(value)), file=f)
		with open(os.path.join(DATA_DIR, 'csr-version-{}.l'.format(vprefix)), 'a') as f:
			for i in range(2):
				if cclass in CSR_CLASSES_RV32:
					print('.*Warning: invalid CSR `{0}\', needs rv32i extension'.format(name), file=f)
				if cclass in CSR_CLASSES_H:
					print('.*Warning: invalid CSR `{0}\', needs `h\' extension'.format(name), file=f)
				if cclass not in CSR_CLASSES_I:
					print('.*Warning: invalid CSR `{0}\', needs {1} extension'.format(name, CSR_EXTENSIONS[cclass]), file=f)
				if nver_k < nver:
					print('.*Warning: invalid CSR `{0}\' for the privileged spec `{1}\''.format(name, k), file=f)
			if is_rdonly:
				print('.*Warning: read-only CSR is written `csrw {},a1\''.format(name), file=f)
