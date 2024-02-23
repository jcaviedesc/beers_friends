from pydantic import BaseModel

class BeerSchema(BaseModel):
    beer_id: int
    qty: int