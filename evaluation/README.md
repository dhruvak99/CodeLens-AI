# CodeLens AI Benchmark Evaluation

Run from the repository root:

```bash
python evaluate.py
```

This generates:

- `benchmark_dataset.json`
- `evaluation_results.json`
- `evaluation_report.md`

The analyzer integration point is:

```python
evaluation/analyzer_adapter.py::analyze_code
```

It calls the existing CodeLens AI backend service:

```python
backend/app/services/analysis_service.py::analysis_service.analyze
```

The adapter returns canonical rule names such as `["UndefinedVariable"]`.
