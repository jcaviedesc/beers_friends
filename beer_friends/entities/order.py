from typing import List

from pydantic import BaseModel

from beer_friends.entities.beer import Beer

class Order(BaseModel):
    beers: List[Beer]
    friend_id: int;
    friend_name: str;