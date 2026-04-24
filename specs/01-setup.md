You are an expert Python backend engineer specializing in FastAPI and AWS AI services. 

I need you to build a production-ready FastAPI microservice that acts as an API gateway for an AWS Bedrock Knowledge Base (RAG system). This API will be consumed by an automation tool (like n8n) to serve B2B client requests.

### Technical Stack & Constraints:
- Framework: FastAPI (Python 3.10+)
- AWS SDK: boto3 bedrock client
- Configuration: Strictly centralized using a single `.env` file and `pydantic-settings`. Do not use `os.getenv()` randomly in the code.
- Server: Uvicorn

### Required Capabilities:
1. A POST endpoint at `/api/rag/query` that accepts a JSON payload with a `prompt` (string) and an optional `session_id` (string).
2. The endpoint must call the AWS Bedrock `RetrieveAndGenerate` API to query a Knowledge Base and generate an answer using an Anthropic Claude model.
3. The response must return the generated `answer` (string) and the `citations` (list) from the Bedrock response.
4. Proper CORS middleware configured to allow external automation tools to call the API.
5. Standardized error handling returning structured HTTP exceptions.

### Project Structure (Please generate the following files):
1. Use UV to generate`project.toml` (include fastapi, uvicorn, boto3, pydantic, pydantic-settings)
2. `.env.example` (template with AWS_REGION, KNOWLEDGE_BASE_ID, MODEL_ARN, and optional AWS credentials for local dev)
3. `config.py` (Define a Pydantic BaseSettings class to load and validate variables from the `.env` file)
4. `schemas.py` (Pydantic models for the QueryRequest and QueryResponse)
5. `aws_client.py` (Initialize the boto3 client using the centralized config)
6. `main.py` (The FastAPI application, CORS setup, and the routing logic)
7. Any aditional file you consider as needed

Please generate the complete code for this microservice.