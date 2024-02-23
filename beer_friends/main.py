from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI()

class Beer(BaseModel):
    name: str
    price: float
    image: str | None = None

class Order(BaseModel):
    beers: List[Beer]

class Bill(BaseModel):
    total: float

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
    This function lists all the available beers.
    """
    return beers

@app.post("/order", response_model=Order)
async def receive_order(order: Order):
    orders.append(order)
    return order

@app.get("/bill", response_model=Bill)
async def get_bill():
    total = sum(beer.price for order in orders for beer in order.beers)
    return Bill(total=total)

@app.post("/pay")
async def pay_bill(beer_name: str):
    for order in orders:
        for beer in order.beers:
            if beer.name == beer_name:
                order.beers.remove(beer)
                return {"message": f"Paid"}
    return {"message": "Beer not found in orders"}