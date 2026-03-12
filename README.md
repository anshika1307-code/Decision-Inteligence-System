# Multi-Agent Decision Intelligence System

A production-ready, domain-specific decision intelligence platform that processes complex business queries through multi-agent orchestration, hybrid retrieval, and structured reasoning.

## Features

- **Multi-Agent Orchestration**: LangGraph-based supervisor with specialized agents (Research, Risk, Financial, Fact-Check, Summary)
- **Hybrid Retrieval**: Vector search (Qdrant) + BM25 keyword search + reranking
- **Structured Output**: Comprehensive decision reports with reasoning traces
- **Production-Grade**: Full observability (logging, metrics, tracing), evaluation (RAGAS), cost optimization
- **Domain-Agnostic**: Handles market analysis, expansion decisions, regulatory impact, risk assessment, competitive analysis

## Requirements

- Python 3.11+
- Docker & Docker Compose (for development)
- OpenAI API key
- Anthropic API key (optional, for fact-checking)
- Cohere API key (optional, for reranking)

## Quick Start

### 1. Clone and Setup

```bash
cd decision-intelligence-system
cp .env.example .env
# Edit .env with your API keys
```

### 2. Install Dependencies

```bash
# Install Poetry
pip install poetry

# Install dependencies
poetry install
# Or
C:\Users\user\AppData\Local\Python\pythoncore-3.14-64\Scripts\poetry.exe install
```

### 3. Start Infrastructure

```bash
# Start Qdrant, Redis, PostgreSQL, Prometheus, Grafana
docker-compose -f deployment/docker/docker-compose.yml up -d
```

### 4. Initialize Database

```bash
# Setup vector database
poetry run python scripts/setup_vector_db.py

# Index documents
poetry run python scripts/index_documents.py
```

### 5. Run API Server

```bash
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Test the System

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Should an Indian SaaS startup expand to UAE?",
    "options": {
      "depth": "comprehensive",
      "include_reasoning": true,
      "max_sources": 20
    }
  }'
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=html

# Run specific test suite
poetry run pytest tests/unit/agents/
poetry run pytest tests/integration/
```

## Evaluation

```bash
# Run RAGAS evaluation
poetry run python scripts/evaluate_system.py

# Run performance benchmark
poetry run python scripts/benchmark.py
```

## Deployment

### Docker

```bash
# Build image
docker build -f deployment/docker/Dockerfile -t decision-intelligence:latest .

# Run container
docker run -p 8000:8000 --env-file .env decision-intelligence:latest
```

## Monitoring

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **API Metrics**: http://localhost:8000/api/v1/metrics

## Documentation

- [Architecture Design](docs/architecture.md)


## Performance Targets

- **Latency**: P95 < 10 seconds
- **Cost**: < $0.50 per query
- **Evaluation**: RAGAS faithfulness > 0.85
- **Uptime**: 99.5%

## License

MIT License

## Support

For issues and questions, please open a GitHub issue.
