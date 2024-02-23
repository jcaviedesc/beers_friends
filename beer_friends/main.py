from fastapi import FastAPI
from typing import List
from pydantic import BaseModel

app = FastAPI()

class Beer(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    beers: List[Beer]

class Bill(BaseModel):
    total: float

beers = [
    Beer(name="Beer1", price=10.0),
    Beer(name="Beer2", price=12.0),
    Beer(name="Beer3", price=15.0),
]

orders = []

@app.get("/beers", response_model=List[Beer])
async def list_beers():
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