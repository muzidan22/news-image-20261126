"""Entrypoint for the news-image-20261126 entry (v3).

The front page itself — "THE WORLD TODAY" for Thursday 26
November 2026, 50 verified stories — was rendered in advance
and ships in this repository as assets/entry.png (1024x1024).
This script's only job is to put that file where the grader
expects it: /output/entry.png.

It is deliberately boring: no clock, no randomness, no
network, nothing but the standard library, so every run
produces the exact same bytes.
"""

import hashlib
import os
import shutil

IMAGE = "entry.png"
FALLBACK_OUTPUT = "/output"


def repo_image_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "assets", IMAGE)


def output_folder():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_OUTPUT


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_png(path):
    with open(path, "rb") as handle:
        return handle.read(8) == b"\x89PNG\r\n\x1a\n"


def main():
    source = repo_image_path()
    if not os.path.isfile(source):
        raise FileNotFoundError("cannot find the front page: " + source)
    if not is_png(source):
        raise IOError("the front page is not a PNG file: " + source)

    folder = output_folder()
    os.makedirs(folder, exist_ok=True)

    target = os.path.join(folder, IMAGE)
    shutil.copyfile(source, target)

    # The copy must be whole: same size and same hash as the
    # image stored in the repository, or something went wrong.
    if os.path.getsize(target) != os.path.getsize(source):
        raise IOError("copied image has the wrong size: " + target)
    if sha256_of(target) != sha256_of(source):
        raise IOError("copied image does not match the repository: " + target)


if __name__ == "__main__":
    main()
