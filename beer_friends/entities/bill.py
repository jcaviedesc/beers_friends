from pydantic import BaseModel
from typing import List
from beer_friends.entities.order import Order


class Bill(BaseModel):
    orders: List[Order]
    total: float