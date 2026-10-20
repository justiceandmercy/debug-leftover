# debug-leftover

Find leftover debug statements (`console.log`, `debugger`, `print`, `pdb`, `binding.pry`, ...) in your source code before they ship.

## Description

`debug-leftover` scans a file or directory tree and reports every line that looks like a
leftover debug statement, with file, line, column, severity and the offending snippet. It
supports JavaScript/TypeScript, Python, Ruby, PHP, Go, Swift, Kotlin, Java, Rust and C# out
of the box, skips common build/dependency directories, and can emit JSON for CI pipelines.

## Features

- Multi-language detection with sensible, targeted patterns (high vs. low severity).
- Recursive directory scan that skips `node_modules`, `.git`, `dist`, `build`, `venv`, etc.
- Inline ignore marker: append `debug-leftover: ignore` to any line.
- `--high-only` to focus on the dangerous ones (debugger, pdb, binding.pry, ...).
- `--json` output for tooling/CI integration.
- `--fail` exits non-zero when findings exist, so it can gate commits/PRs.
- `--ext` to restrict to specific extensions; `--ignore-dir` to add ignore dirs.

## Install

```bash
pip install -e .
# or run without installing:
python -m debug_leftover .
```

## Usage

```bash
# scan current directory
debug-leftover

# scan a path
debug-leftover src/

# only high-severity findings
debug-leftover --high-only

# JSON output
debug-leftover --json > findings.json

# gate CI
debug-leftover --fail

# restrict extensions
debug-leftover --ext .py,.js

# ignore a directory
debug-leftover --ignore-dir tmp
```

Example output:

```
src/app.js:12:1  [low] js-console  console.log("debug", user)
src/db.py:45:5   [high] py-breakpoint  breakpoint()

2 finding(s).
```

## Inline ignore

```js
console.log("intentional startup banner"); // debug-leftover: ignore
```

```python
print("banner")  # debug-leftover: ignore
```

## License

MIT
