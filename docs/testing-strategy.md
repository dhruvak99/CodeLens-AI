Goal:
The analyzer must never crash regardless of user input.

Testing levels:
- Unit tests
- Integration tests
- Regression tests

Principles:
- Fail gracefully.
- Invalid code should return errors, not exceptions.
- Partial code should still analyze when possible.