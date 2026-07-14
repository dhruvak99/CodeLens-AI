from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api import (
    analyze_router,
    apply_fix_router,
    explain_router,
    metrics_router,
    runtime_router,
)

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

app = FastAPI(
    title="CodeLens AI API",
    description=(
        "CodeLens AI backend for semantic analysis, code fixes, runtime tracing, "
        "and complexity metrics. Runtime tracing safely interprets a restricted "
        "Python AST subset for visualization and education."
    ),
    version="0.1.0",
)

app.include_router(analyze_router)
app.include_router(explain_router)
app.include_router(apply_fix_router)
app.include_router(runtime_router)
app.include_router(metrics_router)
