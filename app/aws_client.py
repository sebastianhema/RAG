from functools import lru_cache

import boto3
from botocore.client import BaseClient

from app.config import get_settings


@lru_cache
def get_bedrock_client() -> BaseClient:
    settings = get_settings()

    session_kwargs: dict[str, str] = {}
    if settings.aws_profile and str(settings.aws_profile).strip():
        session_kwargs["profile_name"] = str(settings.aws_profile).strip()
    if settings.aws_access_key_id and settings.aws_secret_access_key:
        session_kwargs["aws_access_key_id"] = settings.aws_access_key_id
        session_kwargs["aws_secret_access_key"] = settings.aws_secret_access_key

    session = boto3.Session(**session_kwargs)
    return session.client("bedrock-agent-runtime", region_name=settings.aws_region)
