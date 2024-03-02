from typing import Optional

from pydantic import BaseModel


class EmailContentType(BaseModel):
    subject: Optional[str] = None
    content: str = None
    cc: Optional[list[str]] = []
    bcc: Optional[list[str]] = []
