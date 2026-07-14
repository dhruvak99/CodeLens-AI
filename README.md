# CodeLens AI

CodeLens AI is an AI-powered learning platform with two workspaces:

- **Python Lab** for semantic analysis, runtime tracing, complexity metrics, suggested fixes, and AI explanations.
- **SQL Lab** for natural-language SQL generation, schema exploration, SQL validation, live query execution, and AI tutoring.

## Features

- Python semantic analysis and findings
- Safe Python runtime visualization
- Complexity and maintainability metrics
- Deterministic code fixes
- SemanticSQL-backed SQL learning workflow
- Dedicated SQL Tutor explanations through Ollama

## Technology Stack

- **Frontend:** Next.js, TypeScript, Tailwind CSS, React Query, Monaco Editor, React Flow
- **Python Backend:** FastAPI, Pydantic, NetworkX
- **SQL Backend:** FastAPI, SQLAlchemy, SQLite, sqlglot, Ollama
- **AI Runtime:** Ollama models `llama3.1` and `qwen2.5:7b`

## Quick Start

```bash
git clone https://github.com/dhruvak99/CodeLens-AI.git
cd CodeLens-AI

chmod +x setup.sh run.sh stop.sh status.sh

./setup.sh
```

Start Ollama in a separate terminal:

```bash
ollama serve
```

Run the application:

```bash
./run.sh
```

Open:

- Frontend: http://localhost:3000
- Python API: http://localhost:8000
- SQL API: http://localhost:8001

Stop managed services:

```bash
./stop.sh
```

Check status:

```bash
./status.sh
```

## Manual Setup

Python backend:

```bash
cd backend
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

SQL backend:

```bash
cd sql_backend
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Frontend:

```bash
cd frontend
npm install
npm run dev -- --hostname 127.0.0.1 --port 3000
```

Ollama models:

```bash
ollama pull llama3.1
ollama pull qwen2.5:7b
```
