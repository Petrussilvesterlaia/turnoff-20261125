#!/usr/bin/env python3
"""turnoff-20261125 — entry for "Have You Tried Turning It Off?" (make.fun).

Writes a single funny line from a hopeless tech support agent to a
desperate customer to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).
Deterministic, no network, no secrets, reads no files outside this repo.
"""

import os
import sys

ENTRY = (
    "Great news — I found the problem: it's your computer, and the fix is "
    "turning it off, turning it on, and then turning *me* off and on again."
)

MIN_LEN = 1
MAX_LEN = 199


def validate(text: str) -> None:
    if not (MIN_LEN <= len(text) <= MAX_LEN):
        raise ValueError(
            f"entry must be {MIN_LEN}-{MAX_LEN} characters, got {len(text)}"
        )
    if not text.strip():
        raise ValueError("entry must not be whitespace only")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry must not contain control characters")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")


def main() -> int:
    try:
        validate(ENTRY)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY)
    # Round-trip check: what landed on disk must be exactly the entry.
    with open(out_path, "r", encoding="utf-8", newline="") as fh:
        if fh.read() != ENTRY:
            print("round-trip mismatch: entry.txt differs from ENTRY",
                  file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
