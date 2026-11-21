#!/usr/bin/env python3
"""Entrypoint: regenerate the front page and place it where the grader
looks. Runs draw.build() (pure Pillow, no network, no clock, no
randomness) and writes entry.png next to this file and, when
MAKEFUN_OUTPUT_DIR is set, a byte-identical copy there too.
Stdlib + Pillow only."""
import hashlib
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import draw  # noqa: E402


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    local = os.path.join(base, "entry.png")
    draw.build().save(local, "PNG", optimize=True)
    print("wrote %s (%d bytes, sha256 %s)"
          % (local, os.path.getsize(local), digest(local)))
    dest_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "entry.png")
        if os.path.abspath(dest) != os.path.abspath(local):
            shutil.copyfile(local, dest)
            assert digest(local) == digest(dest), "copy hash mismatch"
            print("copied entry.png to %s" % dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
