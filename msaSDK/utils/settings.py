from fastapi_utils.api_settings import APISettings
from sqlmodel import SQLModel


class MSAAppSettings(APISettings, SQLModel):
    """ MSAAppSettings, inherit APISettings and SQLModel

    Pydantic gives a powerful tool to parse also environment variables and process them with its validators.
    TODO This will be extended with dynaconf

    """
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "msa_app_"
