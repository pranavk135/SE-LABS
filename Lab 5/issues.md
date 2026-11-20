# Issues found in `energy_system.py`

Line numbers refer to the **original** file. Ordered by severity.
Scores: Pylint 6.14 → 10.00, Bandit 1 Medium → 0, Flake8 12 → 0.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `eval()` on user input (Bandit B307, Pylint W0123) | Security (Medium) | 63 | `eval(adjustment)` runs whatever the user types, e.g. `__import__('os').system(...)` = arbitrary code execution. | Replaced with `float(adjustment)` inside `try/except ValueError`; bad input is reported and ignored. |
| Negative readings accepted (no tool flags it) | Bug | 13-14, 55 | `record_reading("M-03", -50)` gave a negative total and a **negative bill (-192.50)**. | `record_reading` raises `ValueError` for negative or non-finite (`nan`/`inf`) units; the demo now shows the rejection. |
| Mutable default argument (Pylint W0102) | Bug | 12 | `history=[]` is created once and shared across every call, so unrelated callers pollute each other's history. | Default is `None`; a new list is created inside. `main` passes its own list so the count stays 3. |
| Bare `except` (Pylint W0702, Flake8 E722) | Bug / Robustness | 44 | Swallows every error (even `KeyboardInterrupt`), hiding real problems. | Catch only `(OSError, json.JSONDecodeError)`. |
| Unclosed files / no encoding (Pylint R1732, W1514) | Resource leak | 42, 48-50 | `open()` without `with`: file handle leaks if an error occurs before `close()`; encoding is platform dependent. | Use `with open(..., encoding="utf-8")` and `json.load` / `json.dump`. |
| `global` rebinding of shared state (Pylint W0603) | Design | 27, 40 | `raise_rates` mutates module rates (so calling it twice **compounds** the increase); `load_meter_data` rebinds `meters`. | `raise_rates(rates, percent)` returns a new tuple from `DEFAULT_RATES`; loading does `meters.clear()` + `update()`. |
| Unused import `sys` (Pylint W0611, Flake8 F401) | Style | 2 | Dead import. | Removed. |
| Missing docstrings (Pylint C0114, C0116) | Documentation | 1, 12, 17, 26, 32, 39, 47, 52 | Module and every function undocumented. | Added concise docstrings. |
| Unnecessary `elif`/`else` after `return` (Pylint R1705) | Style | 19-24 | Redundant branching after return. | Flat `if ... return` chain. |
| Index loop over dict (Pylint C0206) | Style | 34-37 | `for m in meters: meters[m]` double lookup. | List comprehension over `.items()`. |
| `%` string formatting (Pylint C0209) | Style | 59, 60, 66 | Old-style formatting. | f-strings. |
| Missing blank lines (Flake8 E302, E305) | Format | 12, 17, 26, 32, 39, 47, 52, 68 | PEP 8 needs 2 blank lines around top-level defs. | Added. |
| Line too long (Flake8 E501) | Format | 24, 62 | 88 and 86 chars (> 79). | Wrapped the expression; moved the prompt into a variable. |
| `main()` runs on import | Design | 68 | Importing the module runs the program (blocks tests on `input()`). | `if __name__ == "__main__":` guard. |

## Commits

1. `Fix Bandit B307: replace eval() with float() parsing; reject negative readings`
2. `Fix Pylint issues: docstrings, mutable default, globals, bare except, with-open, f-strings, unused import`
3. `Fix Flake8 issues: blank lines, line lengths, __main__ guard; add after reports`

## Not changed (noticed, out of scope)

`main()` never calls `load_meter_data()` at startup, so each run overwrites `meters.json` instead of continuing from it. Left as is to keep the original demo behaviour.
