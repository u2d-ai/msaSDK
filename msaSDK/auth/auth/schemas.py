from msaSDK.admin.utils.translation import i18n as _
from pydantic import validator, SecretStr, BaseModel
from sqlmodel import Field

from .models import UsernameMixin, PasswordMixin, EmailMixin, BaseUser


class BaseTokenData(BaseModel):
    """Pydantic Model for TokenData"""
    id: int
    username: str


class UserLoginOut(BaseUser):
    """Pydantic Response/Output Model for User Login"""
    token_type: str = 'bearer'
    access_token: str = None
    password: SecretStr = None


class UserRegIn(UsernameMixin, PasswordMixin, EmailMixin):
    """User Registration Input Pydantic Model"""
    password2: str = Field(title=_('Confirm Password'), max_length=128)

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match!')
        return v
