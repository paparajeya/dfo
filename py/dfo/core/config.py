# -*- coding: utf-8 -*-
"""
@Author     : Dr Prashant Aparajeya
                Founder & Director @AISimply Ltd
                Computer Vision Scientist
                London, United Kingdom
                
@Copyright  : Copyright 2024 - present
@Project    : Dispersive Flies Optimization (DFO) Algorithm
"""

import os
import secrets
import warnings
import logging

from functools import lru_cache

from pydantic import (
    AnyHttpUrl,
    BeforeValidator,
    RedisDsn,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import Annotated, Any, List, Union
from typing_extensions import Self

from dotenv import load_dotenv

# read env variables from .env file
load_dotenv()


def get_log_mode() -> int:
    log_mode = (
        logging.DEBUG
        if os.getenv("MODE_LOG", "debug").lower() == "debug"
        else logging.INFO
    )
    return log_mode

def parse_cors(v: Any) -> list[str] | str:
    if v == ["*"]:
        return v
    elif isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    PROJECT_NAME: str = "DFO API"
    API_PREFIX: str = "/api/v1"
    VERSION: str = "0.1.0"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # one week

    BACKEND_CORS_ORIGINS: Annotated[
        List[Union[AnyHttpUrl, str]], BeforeValidator(parse_cors)
    ] = ["*"]
    
    # Timezone
    TIMEZONE: str = os.getenv("TIMEZONE", "UTC")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")
    
    # Logger
    LOG_DIR: str = os.getenv("LOG_DIR", "logs/")
    LOG_FILE: str = os.getenv("LOG_FILE", "dfo.log")
    ISSUE_FILE: str = os.getenv("ISSUE_FILE", "issues.log")
    LOG_INTERVAL: str = os.getenv("LOG_INTERVAL", "midnight")
    BACKUP_COUNT: int = int(os.getenv("BACKUP_COUNT", 7))
    LOG_MODE: int = get_log_mode()

    # Redis
    REDIS_SERVER: str = os.getenv("REDIS_SERVER", "changethis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "changethis")
    REDIS_DB: str = os.getenv("REDIS_DB", "0")
    REDIS_EXPIRY: float = float(os.getenv("REDIS_EXPIRY", 3600))

    @computed_field  # type: ignore[misc]
    @property
    def REDIS_URL(self) -> RedisDsn:
        return MultiHostUrl.build(
            scheme="redis",
            password=self.REDIS_PASSWORD,
            host=self.REDIS_SERVER,
            port=self.REDIS_PORT,
            path=self.REDIS_DB,
        )

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("REDIS_SERVER", self.REDIS_SERVER)
        self._check_default_secret("REDIS_PASSWORD", self.REDIS_PASSWORD)

        return self

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
