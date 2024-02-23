from typing import List
from fastapi import FastAPI

from beer_friends.entities.beer import Beer
from beer_friends.entities.bill import Bill
from beer_friends.entities.order import Order

app = FastAPI()

beers = [
    Beer(name="Poker", price=10.0, image="https://jotajotafoods.com/wp-content/uploads/2022/05/CER00034.jpg"),
    Beer(name="Aguila", price=12.0, image="https://restaurantezodiacbenidorm.es/wp-content/uploads/2021/02/Cerveza-Poker-en-Benidorm-450x450.jpg"),
    Beer(name="Club Colombia", price=15.0, image="https://jotajotafoods.com/wp-content/uploads/2022/05/CER00005.jpg"),
    Beer(name="Costeña", price=13.0, image="https://www.univorca.com/wp-content/uploads/2020/07/coste%C3%B1a-cerveza-exportacion-600x600.jpg"),
    Beer(name="Andina", price=11.0, image="https://www.monde-selection.com/wp-content/uploads/2020/05/_XT20031.png"),
    Beer(name="BBC Rubia", price=14.0, image="https://www.bbccerveceria.com/sites/g/files/seuoyk221/files/2022-07/Lager.png"),
]

orders = []

@app.get("/beers", response_model=List[Beer])
async def list_beers():
    """
    This endpoint returns a list of beers avaliable in the bar
    """
    return [beer for beer in beers if beer.qty > 0]

# recive order should minus the qty of the beer save in beers list

@app.post("/order", response_model=Order)
async def receive_order(order: Order):
    for beer in order.beers:
        for i, b in enumerate(beers):
            if b.name == beer.name:
                beers[i].qty -= beer.qty
    orders.append(order)
    return order

@app.get("/bill", response_model=Bill)
async def get_bill(friend_id: int | None= None, total_friends: int | None=1):
    total = sum(beer.price for order in orders for beer in order.beers)
    if friend_id is None:
        # divide the total of the bill by the number of friends and return the amount to pay
        return Bill(total=total/ total_friends)

    order_by_friend = [order for order in orders if order.friend_id == friend_id]
    total = sum(beer.price for order in order_by_friend for beer in order.beers)
    return Bill(total=total)

@app.post("/pay")
async def pay_bill(friend_id: int | None):
    orders = [order for order in orders if order.friend_id != friend_id]
    return {"message": "Bill payed", "pending": sum(beer.price for order in orders for beer in order.beers) }

