from typing import List

from pydantic import BaseModel

from beer_friends.schemas.beer_schema import BeerSchema

class OrderSchema(BaseModel):
    order_id: int
    beers: List[BeerSchema]
    # order by is a friend_id: int;
    orderby: int
    # status is a string literal or enum with the following values: "pending", "paid"
    status: str = "pending" # default value is "pending"