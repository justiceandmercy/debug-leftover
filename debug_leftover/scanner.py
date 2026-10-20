"""Walk files and find leftover debug statements."""

from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Optional, Set

from .patterns import EXT_TO_LANG, RULES, IGNORE_MARKER

DEFAULT_IGNORE_DIRS = {
    ".git", "node_modules", "vendor", "dist", "build", "target",
    "__pycache__", ".venv", "venv", ".tox", ".mypy_cache",
    ".pytest_cache", "coverage", ".next", ".nuxt", ".turbo",
}

SEV_RANK = {"high": 0, "low": 1}


@dataclass
class Finding:
    path: str
    line: int
    column: int
    rule: str
    severity: str
    description: str
    snippet: str

    def to_dict(self):
        return asdict(self)


def iter_files(root, ignore_dirs: Set[str], include_exts: Optional[Set[str]] = None) -> Iterable[Path]:
    root = Path(root)
    if root.is_file():
        yield root
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in ignore_dirs)
        for fn in sorted(filenames):
            p = Path(dirpath) / fn
            if p.suffix.lower() not in EXT_TO_LANG:
                continue
            if include_exts and p.suffix.lower() not in include_exts:
                continue
            yield p


def scan_file(path, min_severity: str = "low") -> List[Finding]:
    findings: List[Finding] = []
    lang = EXT_TO_LANG.get(Path(path).suffix.lower())
    if lang is None:
        return findings
    rules = RULES.get(lang, [])
    if not rules:
        return findings
    min_rank = SEV_RANK.get(min_severity, 1)
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return findings
    for i, line in enumerate(text.splitlines(), 1):
        if IGNORE_MARKER in line:
            continue
        for rule in rules:
            if SEV_RANK[rule.severity] > min_rank:
                continue
            m = rule.regex.search(line)
            if m:
                findings.append(Finding(
                    path=str(path), line=i, column=m.start() + 1,
                    rule=rule.id, severity=rule.severity,
                    description=rule.description,
                    snippet=line.strip()[:120],
                ))
                break  # one finding per line
    return findings


def scan(root, ignore_dirs=None, include_exts=None, min_severity="low") -> List[Finding]:
    ignore_dirs = set(ignore_dirs) if ignore_dirs else set(DEFAULT_IGNORE_DIRS)
    all_findings: List[Finding] = []
    for p in iter_files(root, ignore_dirs, include_exts):
        all_findings.extend(scan_file(p, min_severity))
    return all_findings
