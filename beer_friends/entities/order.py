from typing import List

from pydantic import BaseModel

from beer_friends.entities.beer import Beer

class Order(BaseModel):
    order_id: int
    beers: List[Beer]
    # order by is a friend_id: int;
    orderby: int
    # status is a string literal or enum with the following values: "pending", "paid"
    status: str = "pending" # default value is "pending"