from pydantic import BaseModel

class Beer(BaseModel):
    name: str
    price: float
    image: str | None = None
    qty: int = 30