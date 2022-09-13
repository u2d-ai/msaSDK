# -*- coding: utf-8 -*-
"""Module for the MSAFile Pydantic Model.


"""

from sqlmodel import SQLModel

"""str: Module Version"""
from typing import Optional


class MSAFile(SQLModel):
    """ MSAFile Model, used for File Import/Upload."""
    filename: Optional[str] = None
    """Internal Safe Name of the file."""
    content_type: Optional[str] = None
    """ Content Mime Type ``pdf`` etc."""
    upload_filename: Optional[str] = None
    """Upload Filename."""
    type_raw: Optional[str] = None
    """Raw Mime Type."""
    type_description: Optional[str] = None
    """Raw Mime Type description."""
    size: int = 0
    """Filesize in bytes."""
    uid: Optional[str] = None
    """GUID for the file."""
