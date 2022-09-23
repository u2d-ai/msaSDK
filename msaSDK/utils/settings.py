from fastapi_utils.api_settings import APISettings
from pydantic import BaseModel


class MSAAppSettings(APISettings, BaseModel):
    """MSAAppSettingsbase, inherit APISettings and BaseModel

    Pydantic gives a powerful tool to parse also environment variables and process them with its validators.
    """

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "msa_app_"
