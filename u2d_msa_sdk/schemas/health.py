from typing import Optional

from pydantic import BaseModel


class MSAHealthDefinition(BaseModel):
    path: str = "/healthcheck"
    interval: Optional[int] = 60