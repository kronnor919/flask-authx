from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError

from flask_authx.domain.errors import ConfigurationError


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    SUPERUSER_NAME: str
    SUPERUSER_PASSWORD: str


try:
    config = Config()  # pyright: ignore[reportCallIssue]

except ValidationError as ex:
    errors = ex.errors(include_context=False, include_url=False)
    msg = f"Missing fields in environment file: {', '.join([str(e['loc'][0]) for e in errors])}"

    raise ConfigurationError(msg)
