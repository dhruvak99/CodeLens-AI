# CodeLens AI - Bug Tracker

## Bug 1
Date: 2026-06-30
Severity: Low
Status: Open

Description:
Duplicate graph edges are generated for repeated definitions.

Input:
x = 10

while x > 0:
    x += 1

Expected:
Only one "defines" edge between global and x.

Actual:
Two identical "defines" edges are generated.

Recommendation:
Deduplicate edges in graph_builder.py.

---

## Bug
Severity: Medium
Status: Deferred to v2

Description:
Complex Python source files may produce false positives inside:

- comprehensions
- generator expressions
- advanced type annotations

Example:
Pasting complexity_engine.py reports undefined variables like
'node' and 'function'.

Recommendation:
Improve scope handling for comprehensions and annotation contexts.


## Bug
Date: 2026-07-01
Severity: High
Status: Fix Before Demo

Description:
Loop iterator variables are not added to the symbol table.

Input:

for i in range(n):
    print(i)

Expected:
Only 'n' should be undefined.

Actual:
'n' and 'i' are both reported as undefined.

Recommendation:
Register ast.For.target as a variable definition in the semantic extractor.