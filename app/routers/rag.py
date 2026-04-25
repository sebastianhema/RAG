from fastapi import APIRouter, Depends

from app.deps import verify_api_key
from app.schemas import QueryRequest, QueryResponse
from app.services import run_rag_query

router = APIRouter(prefix="/api/rag", tags=["rag"])


@router.post("/query", response_model=QueryResponse, dependencies=[Depends(verify_api_key)])
def query_rag(request: QueryRequest) -> QueryResponse:
    return run_rag_query(prompt=request.prompt, session_id=request.session_id)
