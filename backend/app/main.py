from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)
app.include_router(explain_router)
app.include_router(apply_fix_router)
app.include_router(runtime_router)
app.include_router(metrics_router)
