# -*- coding: utf-8 -*-
__version__ = '0.0.3'

from typing import Dict, List, Optional
from pydantic import BaseModel


class MSAFile(BaseModel):
    filename: Optional[str] = None
    content_type: Optional[str] = None
    upload_filename: Optional[str] = None
    type_raw: Optional[str] = None
    type_description: Optional[str] = None
    size: int = 0
    uid: Optional[str] = None
