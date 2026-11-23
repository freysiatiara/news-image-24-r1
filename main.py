#!/usr/bin/env python3
"""Entry point for the news-image-20261124 bounty (round 1).

Copies the pre-rendered front page (entry.png, drawn by draw.py in the
builder session) to /output/entry.png. Standard library only, no network,
fully deterministic: the same bytes are written on every run.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    out = "/output/entry.png"
    os.makedirs("/output", exist_ok=True)
    with open(src, "rb") as f:
        expected = hashlib.sha256(f.read()).hexdigest()
    shutil.copyfile(src, out)
    with open(out, "rb") as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    if actual != expected:
        print("self-check FAILED: copied bytes differ", file=sys.stderr)
        return 1
    print("wrote /output/entry.png sha256=" + actual)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
