from pydantic import BaseModel

class Beer(BaseModel):
    beer_id: int
    name: str=""
    price: float
    image: str | None = None
    qty: int = 0