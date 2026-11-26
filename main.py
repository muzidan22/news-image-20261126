"""Entry program for news-image-20261126 (v1).

Writes the 1024x1024 front-page image that sums up Thursday
26 November 2026's world news to the output directory.

The image itself is built ahead of time and stored in the repo
at assets/entry.png; this program only copies it to the place
the grader reads, /output/entry.png (or $MAKEFUN_OUTPUT_DIR
when that is set). The copy is byte-for-byte identical on
every run: no randomness, no timestamps, no network, and
only the Python standard library is used.
"""

import os
import shutil


def main():
    # The image lives next to this file, in assets/entry.png.
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "assets", "entry.png")
    if not os.path.isfile(src):
        raise FileNotFoundError("entry image missing: %s" % src)

    # The grader sets MAKEFUN_OUTPUT_DIR; default to /output.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)

    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
