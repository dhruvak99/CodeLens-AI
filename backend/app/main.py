from fastapi import FastAPI

from app.api import (
    analyze_router,
    apply_fix_router,
    explain_router,
    metrics_router,
    runtime_router,
)

app = FastAPI(
    title="CodeLens AI API",
    description=(
        "Contract-first API skeleton for CodeLens AI. Endpoints return mock "
        "responses only; semantic analysis, runtime execution, AI explanation, "
        "fix application, and persistence are not implemented yet."
    ),
    version="0.1.0",
)

app.include_router(analyze_router)
app.include_router(explain_router)
app.include_router(apply_fix_router)
app.include_router(runtime_router)
app.include_router(metrics_router)
