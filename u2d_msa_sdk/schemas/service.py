from typing import Dict, List, Optional
from pydantic import BaseModel

from u2d_msa_sdk.schemas.health import MSAHealthDefinition


class MSAServiceDefinition(BaseModel):
    name: str
    version: str
    host: str
    port: int
    tags: List[str]
    metadata: Optional[Dict]
    healthcheck: MSAHealthDefinition = MSAHealthDefinition()