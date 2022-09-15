from typing import Optional, List

from sqlmodel import SQLModel


class MSAOpenAPIInfo(SQLModel):
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