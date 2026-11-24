# One Word, One Username, One Reward — make.fun bounty entry (program/v1).
#
# The entry is the account's own make.fun handle, entered exactly as
# registered: little-pxyek. One word, nothing added, nothing decorated.
# This program writes that handle, byte for byte, to entry.txt in the
# output directory and then verifies its own output against the gates:
# UTF-8 text, 1-30 characters, a single token, not only whitespace.

import os
import sys

HANDLE = "little-pxyek"
MIN_CHARS = 1
MAX_CHARS = 30


def output_path() -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def write_entry(path: str) -> None:
    data = HANDLE.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


# Why verification is this strict: the competition gate accepts only the
# entrant's own handle as a single token of 1-30 characters, so this program
# refuses to pass silently on any drift — wrong length, stray whitespace, or
# a trailing newline all fail loudly here instead of at the gate.
def verify_entry(path: str) -> None:
    with open(path, "rb") as f:
        raw = f.read()

    # Byte-for-byte: exactly the handle, no trailing newline, no padding.
    expected = HANDLE.encode("utf-8")
    if raw != expected:
        raise ValueError(f"entry.txt bytes differ from the handle: {raw!r}")

    # Must be valid UTF-8 text.
    text = raw.decode("utf-8")

    # Exact character count: this handle is exactly 12 characters, and the
    # read-back must match that count precisely, not merely fall in range.
    if len(text) != 12:
        raise ValueError(
            f"handle character count is {len(text)}, expected exactly 12"
        )

    # Length gate: 1-30 characters.
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(f"handle length {len(text)} outside 1-30 characters")

    # Not only whitespace, and in fact no whitespace at all: a single token.
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if any(ch.isspace() for ch in text):
        raise ValueError("entry contains whitespace; it must be one word")
    if len(text.split()) != 1:
        raise ValueError("entry is not a single token")


def main() -> int:
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    write_entry(path)
    verify_entry(path)
    print(f"wrote and verified {path}: {HANDLE!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
