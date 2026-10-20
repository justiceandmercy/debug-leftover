"""Command-line interface for debug-leftover."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .scanner import scan, DEFAULT_IGNORE_DIRS


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="debug-leftover",
        description="Find leftover debug statements (console.log, debugger, print, pdb, ...) before they ship.",
    )
    parser.add_argument("path", nargs="?", default=".", help="file or directory to scan (default: .)")
    parser.add_argument("--ext", help="comma-separated extensions to include, e.g. .py,.js")
    parser.add_argument("--high-only", action="store_true", help="only report high-severity findings")
    parser.add_argument("--json", action="store_true", dest="as_json", help="output findings as JSON")
    parser.add_argument("--fail", action="store_true", help="exit with status 1 if any findings exist (for CI)")
    parser.add_argument("--ignore-dir", action="append", default=[], help="directory name to ignore (repeatable)")
    args = parser.parse_args(argv)

    include_exts = None
    if args.ext:
        include_exts = {
            (e.strip() if e.strip().startswith(".") else "." + e.strip()).lower()
            for e in args.ext.split(",") if e.strip()
        }

    ignore_dirs = set(DEFAULT_IGNORE_DIRS) | set(args.ignore_dir)
    min_sev = "high" if args.high_only else "low"
    findings = scan(args.path, ignore_dirs=ignore_dirs, include_exts=include_exts, min_severity=min_sev)

    if args.as_json:
        print(json.dumps([f.to_dict() for f in findings], indent=2))
    else:
        for f in findings:
            print(f"{f.path}:{f.line}:{f.column}  [{f.severity}] {f.rule}  {f.snippet}")
        print(f"\n{len(findings)} finding(s).", file=sys.stderr)

    if args.fail and findings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
