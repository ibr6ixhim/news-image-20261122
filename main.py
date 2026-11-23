#!/usr/bin/env python3
"""Entry point for the news-image-20261122 bounty.

Copies the pre-rendered front page (entry.png, produced by render.py from
data/stories.json) to /output/entry.png and verifies its SHA-256.

Standard library only: the grader runs Python 3.13 with no third-party
packages, so this file must not import PIL or anything outside the stdlib.
The image itself is a fixed asset rendered beforehand by render.py; this
program only copies it and checks the checksum.
"""
import hashlib
import os
import sys

EXPECTED_SHA256 = "888675e7c97f3134c622d0273a4e367285b2afc895e721ce338e8045e39b7da5"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print("SHA-256 mismatch: got %s, expected %s" % (digest,
                                                         EXPECTED_SHA256),
              file=sys.stderr)
        return 1
    with open(dst, "wb") as fh:
        fh.write(data)
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
