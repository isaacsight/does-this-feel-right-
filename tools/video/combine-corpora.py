#!/usr/bin/env python3
"""Copy several transcript corpora into one directory for a combined profile.

Exists because a shell one-liner got this wrong once: an `&&` chain broke on an
empty-glob `rm` under zsh, the second corpus never copied, and the "combined"
profile silently returned the larger corpus's numbers unchanged. Identical
output to one of the inputs is the tell.

Usage: python3 combine-corpora.py <out_dir> <prefix>=<glob> [<prefix>=<glob> ...]
"""
import glob as globmod
import os
import shutil
import sys

if len(sys.argv) < 3:
    sys.exit(__doc__)

out = sys.argv[1]
shutil.rmtree(out, ignore_errors=True)
os.makedirs(out, exist_ok=True)

total = 0
for spec in sys.argv[2:]:
    prefix, pattern = spec.split('=', 1)
    files = globmod.glob(pattern)
    if not files:
        sys.exit(f"ERROR: no files matched {pattern!r} — refusing to write a partial combine")
    for f in files:
        shutil.copy(f, os.path.join(out, f'{prefix}_{os.path.basename(f)}'))
    print(f'  {prefix:6s} {len(files):5d} files')
    total += len(files)

on_disk = len(os.listdir(out))
print(f'  total  {total:5d} expected, {on_disk} on disk')
if on_disk != total:
    sys.exit('ERROR: count mismatch — name collision between corpora')
