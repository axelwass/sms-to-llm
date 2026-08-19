# sms-to-llm

A small service that lets a system communicate with an LLM over SMS text messages.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the system design, dependency graph,
provider boundaries, configuration, authorization, and testing strategy.

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

Create your local environment file from the example:

```bash
cp .env.example .env
```

Then edit `.env` and set the values for your machine. The application loads
`.env` automatically when it starts. Keep `.env` local because it may contain
secrets; `.env.example` is the safe template to commit.

## Quality checks

```bash
uv run pytest
uv run pyright
uv run ruff check .
uv run ruff format --check .
```

Integration tests are excluded by default. To run them:

```bash
uv run pytest -m integration
```

## Run locally

```bash
uv run sms-to-llm
```

## Ollama (WSL)

To use the Ollama backend from this project inside WSL, install Ollama in WSL itself.

Install prerequisite:

```bash
sudo apt-get update
sudo apt-get install -y zstd
```

Install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Start Ollama and pull a small test model:

```bash
ollama serve
ollama pull tinyllama:1.1b
```

Configure the app (for example in `.env`):

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=tinyllama:1.1b
OLLAMA_TIMEOUT_SECONDS=90
OLLAMA_MAX_TOKENS=80
SYSTEM_PROMPT_PATH=prompts/system_prompt.md
```

Cold start note:

- The first Ollama request after loading a model can take longer in WSL.
- Increase `OLLAMA_TIMEOUT_SECONDS` (for example to `120`) if you still see timeouts.