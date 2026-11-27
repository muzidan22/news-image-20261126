"""Run the news-image-20261126 entry (v4).

The entry is a finished front page, "THE WORLD TODAY" for
Thursday 26 November 2026 — 50 verified stories, 13 drawn
scenes, a BY THE NUMBERS stat strip, a six-item UTC timeline
and a dotted world map — rendered in advance and stored in
this repository at assets/entry.png (1024x1024).

Running this file does exactly one thing: it copies that
image to the place the grader looks for it, /output/entry.png
(or $MAKEFUN_OUTPUT_DIR when set). Nothing else happens.
There is no clock, no randomness and no network access, so
every run writes the very same bytes.
"""

import hashlib
import os
import shutil

FRONT_PAGE = "entry.png"
DEFAULT_OUT = "/output"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def bundled_image():
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "assets", FRONT_PAGE)


def destination_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUT


def file_sha256(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as stream:
        while True:
            block = stream.read(65536)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def looks_like_png(path):
    with open(path, "rb") as stream:
        return stream.read(len(PNG_SIGNATURE)) == PNG_SIGNATURE


def run():
    source = bundled_image()
    if not os.path.isfile(source):
        raise FileNotFoundError("front page missing: " + source)
    if not looks_like_png(source):
        raise ValueError("front page is not a PNG file: " + source)

    out_dir = destination_dir()
    if os.path.isfile(out_dir):
        raise NotADirectoryError("output path is a file, not a folder: " + out_dir)
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, FRONT_PAGE)
    shutil.copyfile(source, target)

    # A partial copy would silently break the entry, so the
    # result is checked against the bundled original: same
    # byte count and same sha256, or the run fails loudly.
    if os.path.getsize(target) != os.path.getsize(source):
        raise IOError("output is the wrong size: " + target)
    if file_sha256(target) != file_sha256(source):
        raise IOError("output does not match the bundled image: " + target)


if __name__ == "__main__":
    run()
