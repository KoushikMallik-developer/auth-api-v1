from abc import ABC

from fastapi import HTTPException


class APIBaseException(ABC, HTTPException):
    def __init__(self, name: str, detail: str, status: int):
        self.detail = detail
        self.name = name
        self.status = status
        super().__init__(status_code=status, detail=detail)
