# -*- coding: utf-8 -*-

import os
from functools import lru_cache

from fastapi_users.authentication import JWTStrategy, BearerTransport, CookieTransport, AuthenticationBackend

if __name__ == '__main__':
    pass


def getSecretKey():
    ret_key: str = os.getenv("SECRET_KEY_SECURITY", "documentunderstandingaiservicex_#M8A{1o3Bd?<ipwt^K},Z)OE<Fkj-X9IILWq|Cf`Y:HFI~&2L%Ion3}+p{T%")
    return ret_key


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=getSecretKey(), lifetime_seconds=86400)


class MSASecurity:

    def __init__(self) -> None:
        super().__init__()
        self.auth_backends = []
        self.bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
        self.cookie_authentication = CookieTransport(cookie_name="sduaiservices-cookie")
        self.auth_backend_jwt = AuthenticationBackend(
            name="jwt_bearer",
            transport=self.bearer_transport,
            get_strategy=get_jwt_strategy,
        )

        self.auth_backend_cookie = AuthenticationBackend(
            name="jwt_cookie",
            transport=self.cookie_authentication,
            get_strategy=get_jwt_strategy,
        )

        self.auth_backends.append(self.auth_backend_jwt)
        self.auth_backends.append(self.auth_backend_cookie)


@lru_cache()
def getMSASecurity() -> MSASecurity:
    """
    This function returns a cached instance of the MSASecurity object.
    Note:
        Caching is used to prevent re-reading the environment every time the MSASecurity is used.
    """
    return MSASecurity()










