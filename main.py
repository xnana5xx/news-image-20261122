#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261122.

Writes the committed front-page image (assets/entry.png), which sums up
the world news of Sunday 22 November 2026, to the output path the
grader expects (/output/entry.png). The copy is byte-for-byte
deterministic: same input file, same output bytes, no network,
standard library only.
"""

import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "entry.png")


def main():
    if not os.path.isfile(SOURCE):
        raise SystemExit(f"committed image missing: {SOURCE}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    # The gate reads exactly these bytes; fail loudly if the copy drifted.
    with open(SOURCE, "rb") as fh:
        expected = fh.read()
    if not expected.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit("committed image is not a whole PNG file")
    # Read the IHDR dimensions: the gate caps the image at 1024x1024.
    width = int.from_bytes(expected[16:20], "big")
    height = int.from_bytes(expected[20:24], "big")
    if width > 1024 or height > 1024:
        raise SystemExit(f"committed image is {width}x{height}, over the 1024x1024 gate limit")
    if len(expected) > 1048576:
        raise SystemExit("committed image exceeds the 1 MiB gate limit")
    with open(target, "rb") as fh:
        if fh.read() != expected:
            raise SystemExit("copied image does not match the committed one")
    print(f"wrote {target} ({len(expected)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
