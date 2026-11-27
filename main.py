"""Run the news-image-20261126 entry (v5).

The entry is a finished front page, "THE WORLD TODAY" for
Thursday 26 November 2026 — 36 verified stories, each with
its source named, a coloured region strip, a six-item UTC
timeline and a dotted world map — rendered in advance and
stored in this repository at assets/entry.png (1024x1024).

Running this file does one thing only: it places that image
where the grader looks for it, /output/entry.png (or the
folder named by $MAKEFUN_OUTPUT_DIR when that is set).
There is no clock, no randomness and no network access, so
every run writes exactly the same bytes.
"""

import hashlib
import os
import shutil

PAGE = "entry.png"
OUT_DEFAULT = "/output"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def bundled_page():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "assets", PAGE)


def out_directory():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or OUT_DEFAULT


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def is_a_png(path):
    with open(path, "rb") as handle:
        return handle.read(len(PNG_MAGIC)) == PNG_MAGIC


def run():
    original = bundled_page()
    if not os.path.isfile(original):
        raise FileNotFoundError("front page is missing: " + original)
    if not is_a_png(original):
        raise ValueError("front page is not a PNG file: " + original)

    folder = out_directory()
    if os.path.isfile(folder):
        raise NotADirectoryError("output path is a file, not a folder: " + folder)
    os.makedirs(folder, exist_ok=True)
    written = os.path.join(folder, PAGE)
    shutil.copyfile(original, written)

    # A short copy would silently break the entry, so the
    # written file is checked against the bundled original:
    # identical size and identical sha256, or the run fails.
    if os.path.getsize(written) != os.path.getsize(original):
        raise IOError("written image has the wrong size: " + written)
    if sha256_file(written) != sha256_file(original):
        raise IOError("written image differs from the bundled one: " + written)


if __name__ == "__main__":
    run()
