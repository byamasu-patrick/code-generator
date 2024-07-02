import os
from typing import ClassVar, List, Optional, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

is_pull_request: bool = os.environ.get("IS_PULL_REQUEST") == "true"
is_preview_env: bool = os.environ.get("IS_PREVIEW_ENV") == "true"

class AppConfig(BaseSettings):
    """
    Config for settings classes that allows for
    combining Settings classes with different env_prefix settings.
    """
    env_prefix: ClassVar[str] = "PREVIEW_" if is_pull_request or is_preview_env else ""

    case_sensitive: ClassVar[bool] = True

    @classmethod
    def prepare_field(cls, field) -> None:
        if "env_names" in field.field_info.extra:
            return
        return super().prepare_field(field)

class AppEnvironment(str, Enum):
    """
    Enum for app environments.
    """
    LOCAL = "local"
    PREVIEW = "preview"
    PRODUCTION = "production"

class PreviewPrefixedSettings(BaseSettings):
    """
    Settings class that uses a different env_prefix for PR Preview deployments.
    """
    CACHE_PREFIX: str = "chroma_cache"
    OPENAI_API_KEY: str

    class Config(AppConfig):
        env_prefix: ClassVar[str] = "PREVIEW_" if is_pull_request or is_preview_env else ""

class Settings(PreviewPrefixedSettings):
    """
    Application settings.
    """
    PROJECT_NAME: str = "Code Generator"
    VECTOR_STORE_PROVIDER: str = "chroma"
    CHROMA_COLLECTION: str = "default"
    CHROMA_PATH: str = "storage/chromadb"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    LOG_LEVEL: str = "INFO"
    IS_PULL_REQUEST: bool = is_pull_request
    RENDER: bool = False

    @property
    def VERBOSE(self) -> bool:
        """
        Used for setting verbose flag in LlamaIndex modules.
        """
        return self.LOG_LEVEL == "DEBUG" or self.IS_PULL_REQUEST or not self.RENDER

    @property
    def S3_ENDPOINT_URL(self) -> Optional[str]:
        """
        Used for setting S3 endpoint URL in the s3fs module.
        """
        return None if self.RENDER else "http://localhost:4566"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("LOG_LEVEL", pre=True, check_fields=False)
    def assemble_log_level(cls, v: str) -> str:
        """
        Preprocesses the log level to ensure its validity.
        """
        v = v.strip().upper()
        if v not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("Invalid log level: " + str(v))
        return v

    @validator("IS_PULL_REQUEST", pre=True, check_fields=False)
    def assemble_is_pull_request(cls, v: str) -> bool:
        """
        Preprocesses the IS_PULL_REQUEST flag.
        """
        if isinstance(v, bool):
            return v
        return v.lower() == "true"

    @property
    def ENVIRONMENT(self) -> AppEnvironment:
        """
        Returns the app environment.
        """
        if self.RENDER:
            if self.IS_PULL_REQUEST:
                return AppEnvironment.PREVIEW
            else:
                return AppEnvironment.PRODUCTION
        else:
            return AppEnvironment.LOCAL

    @property
    def UVICORN_WORKER_COUNT(self) -> int:
        if self.ENVIRONMENT == AppEnvironment.LOCAL:
            return 1
        return 3

    @property
    def SENTRY_SAMPLE_RATE(self) -> float:
        """
        Sample rate for Sentry.
        """
        return 0.07 if self.ENVIRONMENT == AppEnvironment.PRODUCTION else 1.0

    class Config(AppConfig):
        env_prefix: ClassVar[str] = ""

settings = Settings()
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
