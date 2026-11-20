#!/usr/bin/env python3
"""news-image-20261120 entry (Python 3.13, standard library only).

The entry image is entry.png beside this file, drawn by make_poster.py from
the world news of Friday 20 November 2026. The program copies it to
/output/entry.png, so the run is deterministic and needs no network.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(DST_DIR, exist_ok=True)
dst = os.path.join(DST_DIR, "entry.png")
shutil.copyfile(SRC, dst)
# Sanity check: the output must be a whole PNG (magic bytes), as the gate
# requires. Fail loudly here rather than shipping a broken file.
with open(dst, "rb") as f:
    assert f.read(8) == b"\x89PNG\r\n\x1a\n", "entry.png is not a PNG"
print("wrote", dst)
