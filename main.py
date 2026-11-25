"""The Excuse That Almost Works: write the one line a gamer texts the boss
to skip work on GTA 6 launch week.

The line is fixed. It leans on the judge brief: a tired manager who has
heard every excuse twice and believes almost none of them. So the excuse
is a real, specific, boring workplace-adjacent detail - a landlord replacing
the front door, the writer locked IN until the locksmith finishes at noon -
not a wild story, not the obvious dead grandmother, flat tyre, or sudden
fever. The laugh comes from the excuse's own logic (locked in by your own
door being replaced), and it reads like a text sent in a hurry: one line,
plain words, no setup, no explanation, no signature. 17 words, 100 chars.

No input, no randomness, no network, no time dependence. The program writes
the line to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output), then verifies
what landed on disk byte for byte and re-checks the gate on the disk copy.
"""

import os
import sys

LINE = "My landlord's replacing the front door today and I'm locked in until the locksmith finishes at noon."

MAX_CHARS = 140
MAX_WORDS = 20


def check_gate(text):
    """Mirror the sealed gate: UTF-8 text, 1-140 chars, not only whitespace,
    exactly one line, at most 20 words."""
    if not isinstance(text, str):
        return "not text"
    if len(text) < 1 or len(text) > MAX_CHARS:
        return "length %d outside 1-%d chars" % (len(text), MAX_CHARS)
    if not text.strip():
        return "only whitespace"
    if "\n" in text or "\r" in text:
        return "more than one line"
    if len(text.split()) > MAX_WORDS:
        return "more than %d words" % MAX_WORDS
    return None


def main():
    problem = check_gate(LINE)
    if problem:
        print("gate FAIL on fixed line: %s" % problem, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        on_disk = f.read()
    if on_disk != data:
        print("round-trip FAIL: disk bytes differ", file=sys.stderr)
        return 1
    if on_disk.endswith(b"\n"):
        print("trailing newline FAIL", file=sys.stderr)
        return 1
    problem = check_gate(on_disk.decode("utf-8"))
    if problem:
        print("gate FAIL on disk copy: %s" % problem, file=sys.stderr)
        return 1
    print(LINE)
    print("chars: %d, words: %d" % (len(LINE), len(LINE.split())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
