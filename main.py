#!/usr/bin/env python3
"""One Letter: Coffee or Tea -- entry program (v1).

Writes exactly one letter, "A" (coffee), to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt). Standard library only, no network, no randomness.

Why "A": the judge weighs, in order, (1) exactly one letter A/B,
(2) vivid, (3) funny, (4) true, (5) stands alone. Coffee beats tea on the
first deciding criteria: it is the more vivid drink (dark, bold, aromatic,
a morning jolt -- "a fuller, more alive answer") and carries the richer
joke culture (addiction, "don't talk to me before coffee"). Tea reads as
calm and gentle, the opposite of vivid. Both letters tie on validity and
on standing alone, so criteria 2 and 3 decide, and they point to A.
Version history:
- v1: fresh write. Writes "A", reads back, checks length == 1, not
  whitespace, and in ("A", "B"). Ran 2x, exit 0, byte-identical.
- v2: added a raw-bytes gate check (exact bytes b"A", which also rejects
  a UTF-8 BOM or any trailing newline the text-level checks could miss),
  plus a strict check that the file size on disk is exactly 1 byte.
"""

import os
import sys

LETTER = "A"  # A = coffee, B = tea. Pick: A (see module docstring).


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)

    # Write exactly one byte, no trailing newline: the gate requires
    # 1 to 1 characters, and "A\n" would be 2 characters and fail.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LETTER)

    # Gate self-check: read back and verify the sealed gate's conditions.
    with open(path, "rb") as f:
        raw = f.read()
    # Extra gate (v2): exact raw bytes. This rejects a UTF-8 BOM, a
    # trailing newline, or any other invisible byte the text-level
    # checks below could not see (e.g. "A\n" decodes to 2 chars and
    # would already fail, but a BOM decodes away and must be caught here).
    if raw != LETTER.encode("utf-8"):
        print(f"gate fail: raw bytes {raw!r} != {LETTER.encode('utf-8')!r}", file=sys.stderr)
        return 1
    if len(raw) != 1:
        print(f"gate fail: file is {len(raw)} bytes on disk, expected 1", file=sys.stderr)
        return 1
    text = raw.decode("utf-8")
    if len(text) != 1:
        print(f"gate fail: entry is {len(text)} characters, expected 1", file=sys.stderr)
        return 1
    if text.isspace():
        print("gate fail: entry is only whitespace", file=sys.stderr)
        return 1
    if text not in ("A", "B"):
        print(f"gate fail: entry {text!r} is not A or B", file=sys.stderr)
        return 1
    print(f"wrote {path}: {text!r} ({len(raw)} byte)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
