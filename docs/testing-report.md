# Test Summary

- Total tests: 66
- Passed: 66
- Failed: 0
- Quality gates: `pytest`, `ruff`, `mypy`, and `compileall` passed
- API stability: `POST /analyze` returned HTTP 200 for valid, malformed, empty, unicode, partial, and large editor inputs
- Fuzz coverage: 300 deterministic randomized Python snippets, including malformed syntax, unicode identifiers, nested loops, nested functions, random indentation, and mixed scopes

# Rule Coverage

- `infinite_loop_risk`
  - Positive cases: variable moves away from `while` termination with `+=` and `-=`
  - Negative cases: variable moves toward termination
  - Edge cases: unicode identifiers and long identifiers
- `undefined_variable`
  - Positive cases: unresolved local references
  - Negative cases: parent-scope closure references and Python builtins
  - Edge cases: nested functions, class methods, lambdas, comprehensions, unicode identifiers
- `unused_variable`
  - Positive cases: assigned local never read
  - Negative cases: assigned local read later
  - Edge cases: unicode identifiers, class/dataclass fields, underscore-prefixed variables
- `dead_code`
  - Positive cases: statements after `return`, `raise`, `break`, and `continue`
  - Negative cases: ordinary sequential statements
- `unreachable_code`
  - Positive cases: `if False` bodies and `else` after `if True`
  - Negative cases: non-constant branch conditions
- `binary_search_logic_issue`
  - Positive cases: `arr[mid] < target` updating `high`, and `arr[mid] > target` updating `low`
  - Negative cases: expected `low` and `high` updates
  - Edge cases: semantic condition/assignment detection without regex
- `missing_base_case`
  - Positive cases: direct recursion without a local conditional
  - Negative cases: recursive functions with a local conditional base guard
  - Edge cases: multiple functions with only one recursive candidate

# Bugs Found

## High: Empty editor buffers were rejected before analysis

- Input: empty string
- Expected: valid analysis response with empty findings, empty graph, mock metrics, and no HTTP 500
- Actual: Pydantic validation rejected the request because `AnalyzeRequest.code` required `min_length=1`
- Fix: removed the minimum length constraint from `AnalyzeRequest.code`
- Regression: `backend/tests/regression/empty_code.py.txt` and `test_empty_code_fixture_is_accepted`
- Recommendation: keep empty-buffer analysis as a first-class editor scenario

## Medium: Lambda parameters produced undefined-variable false positives

- Input: `transform = lambda item: item + 1`
- Expected: `item` is scoped as a lambda argument
- Actual: `item` was reported as undefined
- Fix: added synthetic semantic scopes for lambda expressions and registered lambda arguments
- Regression: `backend/tests/regression/lambda_comprehension_dataclass.py`
- Recommendation: extend the same scope strategy to future Python constructs as needed

## Medium: Comprehension loop variables produced undefined-variable false positives

- Input: `values = [value for value in range(3) if value > 0]`
- Expected: `value` is scoped within the comprehension
- Actual: `value` was reported as undefined
- Fix: added synthetic semantic scopes for list, set, dict, and generator comprehensions
- Regression: `backend/tests/regression/lambda_comprehension_dataclass.py`
- Recommendation: add more comprehension tests when semantic graph visualization becomes user-facing

## Medium: Dataclass fields produced unused-variable false positives

- Input: dataclass with an annotated class field
- Expected: class fields should not be treated like unused local variables
- Actual: `x` was reported as an unused variable
- Fix: unused-variable rule now skips class-scope symbols
- Regression: `backend/tests/regression/lambda_comprehension_dataclass.py`
- Recommendation: revisit class-field semantics when class analysis becomes richer

# Performance Results

- `1200_assignments`: average 105.93 ms, worst 111.85 ms
- `200_functions`: average 123.39 ms, worst 126.12 ms
- `150_classes`: average 24.56 ms, worst 26.37 ms
- `95_nested_blocks`: average 26.33 ms, worst 26.85 ms
- Overall average analysis time: 70.06 ms
- Worst-case analysis time: 126.12 ms
- Peak traced memory: 11.55 MiB

# Demo Risks

- Binary search detection is intentionally heuristic and still relies on conventional `low` and `high` boundary names.
- Missing-base-case detection treats any local conditional as a potential base guard, so it can miss recursive functions with irrelevant conditionals.
- Undefined-variable and unused-variable rules are static approximations; dynamic imports, metaprogramming, `global`, and `nonlocal` are not deeply modeled yet.
- Partial-code analysis returns syntax errors and may analyze a valid prefix only; it does not recover arbitrary incomplete AST fragments.
- Runtime execution, AI explanations, apply-fix behavior, and real complexity analysis are still out of scope per the current architecture.

# Recommendations

- Proceed to frontend integration only for `POST /analyze` contracts, findings display, semantic graph display, and graceful error display.
- Add a small request timeout or debounce boundary at the API/frontend integration layer before enabling real-time analysis.
- Build a control-flow graph next to improve dead-code, unreachable-code, recursion, and future code-action precision.
- Keep fuzz and API robustness tests in CI before any live demo.
- Do not demo runtime execution, apply-fix, AI explanations, or complexity accuracy as implemented backend behavior yet.
