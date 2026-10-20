"""Debug-statement patterns grouped by language family."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

IGNORE_MARKER = "debug-leftover: ignore"


@dataclass(frozen=True)
class Rule:
    id: str
    description: str
    regex: re.Pattern
    severity: str  # "high" or "low"


EXT_TO_LANG = {
    ".js": "js", ".mjs": "js", ".cjs": "js", ".jsx": "js",
    ".ts": "js", ".tsx": "js",
    ".py": "py",
    ".rb": "rb",
    ".php": "php",
    ".go": "go",
    ".swift": "swift",
    ".kt": "kt", ".kts": "kt",
    ".java": "java",
    ".rs": "rs",
    ".c": "c", ".cpp": "cpp", ".cc": "cpp", ".h": "cpp", ".hpp": "cpp",
    ".cs": "cs",
}

RULES = {
    "js": [
        Rule("js-debugger", "debugger statement", re.compile(r"\bdebugger\b"), "high"),
        Rule("js-console", "console.* call", re.compile(r"\bconsole\.(log|debug|info|warn|error|trace|dir|table)\s*\("), "low"),
        Rule("js-alert", "alert() call", re.compile(r"\balert\s*\("), "low"),
    ],
    "py": [
        Rule("py-breakpoint", "breakpoint()/pdb", re.compile(r"\b(breakpoint|pdb\.set_trace|ipdb\.set_trace)\s*\("), "high"),
        Rule("py-print", "print() call", re.compile(r"\bprint\s*\("), "low"),
    ],
    "rb": [
        Rule("rb-pry", "binding.pry/byebug", re.compile(r"\b(binding\.pry|byebug)\b"), "high"),
        Rule("rb-puts", "puts/pp call", re.compile(r"\b(puts|pp)\s*\("), "low"),
    ],
    "php": [
        Rule("php-dump", "var_dump/print_r/dd", re.compile(r"\b(var_dump|print_r|dd)\s*\("), "high"),
    ],
    "go": [
        Rule("go-println", "fmt.Println (debug)", re.compile(r"\bfmt\.Println\s*\("), "low"),
    ],
    "swift": [
        Rule("swift-print", "print() call", re.compile(r"\bprint\s*\("), "low"),
    ],
    "kt": [
        Rule("kt-println", "println() call", re.compile(r"\bprintln\s*\("), "low"),
    ],
    "java": [
        Rule("java-println", "System.out.println", re.compile(r"System\.out\.println\s*\("), "low"),
    ],
    "rs": [
        Rule("rs-println", "println! macro", re.compile(r"\bprintln!\s*\("), "low"),
    ],
    "cs": [
        Rule("cs-writeline", "Console.WriteLine", re.compile(r"Console\.WriteLine\s*\("), "low"),
    ],
    "c": [],
    "cpp": [],
}
