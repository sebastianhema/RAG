from botocore.exceptions import ClientError, ProfileNotFound

from app.aws_client import get_bedrock_client
from app.config import get_settings
from app.schemas import Citation, QueryResponse


class AppError(Exception):
    def __init__(self, message: str, detail: str | None = None, status_code: int = 500) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail
        self.status_code = status_code


def _map_bedrock_error(error: ClientError) -> AppError:
    err = error.response.get("Error", {})
    code = err.get("Code", "UnknownError")
    message = err.get("Message", "Unknown Bedrock error")

    mapping = {
        "ValidationException": 400,
        "AccessDeniedException": 403,
        "ResourceNotFoundException": 404,
        "ThrottlingException": 429,
    }
    status_code = mapping.get(code, 502)
    return AppError(message=f"Bedrock request failed: {code}", detail=message, status_code=status_code)


def run_rag_query(prompt: str, session_id: str | None = None) -> QueryResponse:
    settings = get_settings()

    request_payload = {
        "input": {"text": prompt},
        "retrieveAndGenerateConfiguration": {
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": settings.knowledge_base_id,
                "modelArn": settings.model_arn,
            },
        },
    }
    if session_id:
        request_payload["sessionId"] = session_id

    try:
        client = get_bedrock_client()
        response = client.retrieve_and_generate(**request_payload)
    except ClientError as error:
        raise _map_bedrock_error(error) from error
    except ProfileNotFound as error:
        raise AppError(
            "AWS profile configuration error",
            detail=str(error),
            status_code=500,
        ) from error
    except Exception as error:  # pragma: no cover - defensive fallback
        raise AppError("Unexpected error querying Bedrock", detail=str(error), status_code=500) from error

    citations = [
        Citation(
            generated_response_part=item.get("generatedResponsePart"),
            retrieved_references=item.get("retrievedReferences", []),
        )
        for item in response.get("citations", [])
    ]
    return QueryResponse(
        answer=response.get("output", {}).get("text", ""),
        session_id=response.get("sessionId"),
        citations=citations,
    )
