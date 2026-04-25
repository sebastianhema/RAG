from functools import lru_cache
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    aws_region: str = Field(alias="AWS_REGION")
    knowledge_base_id: str = Field(alias="KNOWLEDGE_BASE_ID")
    model_arn: str = Field(alias="MODEL_ARN")

    aws_profile: str | None = Field(default=None, alias="AWS_PROFILE")
    aws_access_key_id: str | None = Field(default=None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str | None = Field(default=None, alias="AWS_SECRET_ACCESS_KEY")

    cors_origins: str = Field(default="*", alias="CORS_ORIGINS")
    api_keys: str = Field(default="", alias="API_KEYS")
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    @property
    def api_keys_set(self) -> set[str]:
        if not self.api_keys.strip():
            return set()
        return {k.strip() for k in self.api_keys.split(",") if k.strip()}

    @property
    def cors_origins_list(self) -> list[str]:
        value = self.cors_origins
        if not value:
            return ["*"]
        return [origin.strip() for origin in value.split(",") if origin.strip()]

    def model_post_init(self, __context: Any) -> None:  # type: ignore[override]
        if self.aws_profile is not None and not str(self.aws_profile).strip():
            self.aws_profile = None
        if self.aws_access_key_id is not None and not str(self.aws_access_key_id).strip():
            self.aws_access_key_id = None
        if self.aws_secret_access_key is not None and not str(self.aws_secret_access_key).strip():
            self.aws_secret_access_key = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
