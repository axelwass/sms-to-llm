# sms-to-llm

A small service that lets a system communicate with an LLM over SMS text messages.

## Stack

- FastAPI
- Pydantic
- Pyright
- Ruff
- Pytest
- uv

## Setup

```bash
uv sync --group dev
```

Optional local shell:

```bash
uv shell
```

## Quality checks

```bash
uv run pytest
uv run pyright
uv run ruff check .
uv run ruff format --check .
```

## API

Current endpoints:

- `GET /version` returns the package version
- `GET /health` returns service status

Example responses:

```json
{
  "version": "0.1.0"
}
```

```json
{
  "status": "ok"
}
```

## Run locally

```bash
uv run fastapi dev src/sms_to_llm/main.py
```

or:

```bash
uv run python -m uvicorn sms_to_llm.main:app --reload
```