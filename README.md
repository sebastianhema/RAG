# Bedrock RAG Gateway

FastAPI microservice that proxies `POST /api/rag/query` requests to AWS Bedrock Knowledge Base `RetrieveAndGenerate`.

## Prerequisites

- Python 3.10+
- `uv` installed
- AWS credentials configured (profile, env vars, or IAM role)

## Setup

```bash
cp .env.example .env
uv sync
```

Update `.env` with your AWS values, especially:

- `AWS_REGION`
- `KNOWLEDGE_BASE_ID`
- `MODEL_ARN`

## Run

```bash
uv run fastapi dev
```

The API starts on `http://127.0.0.1:8000`.

## Endpoints

- `GET /health`
- `POST /api/rag/query`

Example request:

```bash
curl -X POST "http://127.0.0.1:8000/api/rag/query" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"What is our pricing policy?","session_id":"abc-123"}'
```

Example response:

```json
{
  "answer": "Your generated answer",
  "session_id": "abc-123",
  "citations": []
}
```
