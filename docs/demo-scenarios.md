# CodeLens AI - Demo Scenarios

This document contains the official demo scenarios for CodeLens AI v1.

---

# Demo 1 – Undefined Variable Detection

## Input

```python
print(x)
```

## Expected Findings

- Undefined Variable (`x`)

## Purpose

Demonstrates:
- Symbol table generation
- Scope resolution
- Semantic analysis
- Deterministic Apply Fix

## Apply Fix

Click `Apply Fix` on the finding.

Expected updated code:

```python
x = None
print(x)
```

---

# Demo 2 – Infinite Loop Risk Detection

## Input

```python
x = 10

while x > 0:
    x += 1
```

## Expected Findings

- Infinite Loop Risk

## Purpose

Demonstrates:
- Loop analysis
- Variable update tracking
- Rule engine
- Deterministic Apply Fix

## Apply Fix

Click `Apply Fix` on the finding.

Expected updated code:

```python
x = 10

while x > 0:
    x -= 1
```

---

# Demo 3 – Valid Loop (No False Positive)

## Input

```python
x = 10

while x > 0:
    x -= 1
```

## Expected Findings

- No findings

## Purpose

Demonstrates:
- False positive prevention
- Rule precision

---

# Demo 4 – Missing Base Case Detection

## Input

```python
def recurse(n):
    recurse(n - 1)
```

## Expected Findings

- Missing Base Case

## Purpose

Demonstrates:
- Recursive function detection
- Semantic graph generation
- Rule engine
- Deterministic Apply Fix

## Apply Fix

Click `Apply Fix` on the finding.

Expected updated code:

```python
def recurse(n):
    if n <= 0:
        return
    recurse(n - 1)
```

---

# Demo 5 – Valid Recursion

## Input

```python
def recurse(n):
    if n <= 0:
        return
    recurse(n - 1)
```

## Expected Findings

- No findings

## Purpose

Demonstrates:
- Correct base-case detection
- False positive prevention

---

# Demo 6 – Binary Search Logic Issue

## Input

```python
arr = [1, 2, 3]
target = 2
mid = 1
high = 2

if arr[mid] < target:
    high = mid - 1

print(high)
```

## Expected Findings

- Binary Search Logic Issue

## Purpose

Demonstrates:
- Algorithm pattern recognition
- Semantic rule analysis
- Deterministic Apply Fix

## Apply Fix

Click `Apply Fix` on the finding.

Expected updated code:

```python
arr = [1, 2, 3]
target = 2
mid = 1
high = 2

if arr[mid] < target:
    low = mid + 1

print(high)
```

---

# Demo 7 – Syntax Error Handling

## Input

```python
while:
```

## Expected Findings

```text
Syntax Error
Line: 1
Column: 6
```

## Purpose

Demonstrates:
- Parser robustness
- Error handling
- No application crashes

---

# Demo 8 – Unicode Identifier Support

## Input

```python
π = 10

while π > 0:
    π += 1
```

## Expected Findings

- Infinite Loop Risk

## Purpose

Demonstrates:
- Unicode identifier support
- Internationalization
- Rule engine robustness

---

# Demo 9 – Nested Scope Resolution

## Input

```python
def outer():
    x = 10

    def inner():
        print(x)
```

## Expected Findings

- No findings

## Purpose

Demonstrates:
- Closure handling
- Scope resolution
- Symbol table correctness

---

# Demo 10 – Semantic Graph Visualization

## Input

```python
def add(a, b):
    return a + b

x = add(5, 10)
print(x)
```

## Expected Findings

- No findings

## Expected Graph

```text
global
├── add
├── x
└── print
```

## Purpose

Demonstrates:
- AST generation
- Semantic graph construction
- Function call relationships

---

# Demo Order (Presentation)

1. Undefined Variable
2. Apply Fix for Undefined Variable
3. Infinite Loop
4. Apply Fix for Infinite Loop
5. Missing Base Case
6. Apply Fix for Missing Base Case
7. Binary Search Logic Issue
8. Apply Fix for Binary Search Logic Issue
9. Syntax Error
10. Semantic Graph Visualization

---

# Backup Demo Scenarios

- Unicode Identifier Support
- Nested Scope Resolution
- Valid Loop (No False Positive)
- Valid Recursion

---

# Key Points to Mention During Presentation

- Built using Python AST.
- Uses semantic extraction and symbol tables.
- Rule engine operates on semantic information rather than raw source code.
- Includes deterministic rule-based Apply Fix.
- Tested with automated tests, fuzz testing, and regression testing.
- Average analysis time: ~70 ms.
- No HTTP 500 errors during testing.
- Backend demo readiness score: 95%.

---

# Future Work (v2)

- Control Flow Graph (CFG)
- Data Flow Analysis
- Advanced Complexity Analysis
- Runtime Execution Engine
- AI-Powered Fix Suggestions
- Multi-file Analysis
