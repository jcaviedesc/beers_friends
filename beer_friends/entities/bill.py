from pydantic import BaseModel


class Bill(BaseModel):
    total: float