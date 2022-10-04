from typing import List, Optional
from pydantic import BaseModel


class MSAOpenAPIInfo(BaseModel):
    """
    **MSAOpenAPIInfo** Pydantic Response Class
    """

    name: str = "msaSDK Service"
    """Service Name."""
    version: str = "0.0.0"
    """API Version."""
    url: str = "/openapi.json"
    """OpenAPI URL."""
    tags: Optional[List[str]] = None
    """OpenAPI Tags."""
