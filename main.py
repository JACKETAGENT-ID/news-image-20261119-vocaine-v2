#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261119 bounty (vocaine, v2).

The cover image is pre-rendered by generate.py and shipped as
entry.png next to this file. This program only copies it, byte for
byte, into the output directory, so repeated runs are byte-identical.
Standard library only, no network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Sanity check: the copy must be byte-identical to the bundled asset.
    assert os.path.getsize(dst) == os.path.getsize(src), "entry.png copy mismatch"
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
