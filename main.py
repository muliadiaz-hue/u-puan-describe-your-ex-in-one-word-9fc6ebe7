"""Describe Your Ex in One Word — entry generator.

Reads the single-word verdict prepared in entry.txt next to this script,
checks it against the competition's shape rules, and writes the exact
bytes to the output directory make.fun grades from.

Output location honours MAKEFUN_OUTPUT_DIR and falls back to /output.
"""

import os
import sys
from pathlib import Path

MAX_CHARS = 111
OUTPUT_NAME = "entry.txt"


def load_verdict(script_dir: Path) -> bytes:
    """Return the prepared verdict bytes, untouched."""
    source = script_dir / OUTPUT_NAME
    if not source.is_file():
        raise SystemExit(f"missing prepared verdict file: {source}")
    payload = source.read_bytes()
    return payload


def check_verdict(payload: bytes) -> str:
    """Validate the verdict shape; return it decoded for reporting."""
    if len(payload) == 0:
        raise SystemExit("verdict is empty — nothing to submit")
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError:
        raise SystemExit("verdict is not valid UTF-8")
    if len(text) > MAX_CHARS:
        raise SystemExit(
            f"verdict is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if any(ch.isspace() for ch in text):
        raise SystemExit("verdict must be exactly one word, no whitespace")
    return text


def write_verdict(payload: bytes) -> Path:
    """Write the exact verdict bytes to the graded output file."""
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / OUTPUT_NAME
    target.write_bytes(payload)
    # Read the file back: the graded bytes must be exactly what we wrote.
    if target.read_bytes() != payload:
        raise SystemExit(f"round-trip mismatch writing {target}")
    return target


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    payload = load_verdict(script_dir)
    word = check_verdict(payload)
    target = write_verdict(payload)
    print(f"wrote {len(payload)} bytes ({len(word)} chars) to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
