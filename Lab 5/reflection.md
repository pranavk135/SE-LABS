# Reflection

**1. Which issues were the easiest and which the hardest to fix?**
Easiest: the mechanical ones: unused import, f-strings, docstrings, blank lines, `with open`. Hardest: the `global` statements. Removing them meant changing `raise_rates` to take and return rates, and changing `load_meter_data` to update the dict in place, and checking nothing else depended on the old behaviour. `eval` was easy to remove but needed a decision about what input to accept.

**2. Did the tools report any false positives, or miss anything?**
No outright false positives, but some findings are judgement calls: `global-statement` and missing docstrings are style opinions, not bugs, and Bandit's CWE-78 label on `eval` is really code injection. Real misses: the negative reading producing a negative bill is a logic bug no tool flags, and neither is `main()` never loading saved data. Tools find patterns, not intent. Running the program and reading the output caught what they couldn't.

**3. How would you integrate these tools into a development workflow?**
Run Flake8 and Pylint in a pre-commit hook and in CI (e.g. GitHub Actions) on every pull request, failing the build below a Pylint threshold (e.g. 9.5) and on any Bandit Medium/High finding. Editor integration gives instant feedback while typing. Using a formatter such as black removes most Flake8 noise automatically.

**4. What tangible improvements did you see after the fixes?**
Pylint went 6.14 → 10.00, Bandit 1 Medium → 0, Flake8 12 → 0. More importantly: arbitrary code execution through input is gone, invalid data is rejected, history is no longer shared between calls, files are always closed, errors are no longer silently swallowed, and the module can be imported (and tested) without running. The code is also easier to read and review.
