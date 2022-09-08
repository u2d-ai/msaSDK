from pydantic import BaseSettings, Field, validator, root_validator


class AdminSettings(BaseSettings):
    debug: bool = False
    version: str = '0.0.1'
    site_title: str = 'Admin'
    site_icon: str = '/msastatic/img/favicon.png'
    site_url: str = ''
    root_path: str = '/admin'
    database_url_async: str = Field('', env='DATABASE_URL_ASYNC')
    database_url: str = Field('', env='DATABASE_URL')
    language: str = ''  # 'zh_CN','en_US'

    @validator('root_path', 'site_url', pre=True)
    def valid_url(cls, url: str):
        return url[:-1] if url.endswith('/') else url

    @root_validator(pre=True)
    def valid_database_url(cls, values):
        if not values.get('database_url') and not values.get('database_url_async'):
            values.setdefault('database_url', 'sqlite+aiosqlite:///msa_sdk.db?check_same_thread=False')
        return values
