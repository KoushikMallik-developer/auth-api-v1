from typing import Optional, Any
from pydantic import BaseModel


class BaseResponse(BaseModel):
    data: Any = None
    errorMessage: Optional[str] = None
    successMessage: Optional[str] = None
    status_code: Optional[int] = None
