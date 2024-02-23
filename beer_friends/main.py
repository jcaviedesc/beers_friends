from typing import List
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from beer_friends.entities.beer import Beer
from beer_friends.entities.bill import Bill
from beer_friends.entities.order import Order
from beer_friends.schemas.order_schema import OrderSchema

app = FastAPI()

InMemoryBeers = [
    Beer(beer_id=0, name="Poker", price=10.0, image="https://jotajotafoods.com/wp-content/uploads/2022/05/CER00034.jpg", qty=10),
    Beer(beer_id=1, name="Aguila", price=12.0, image="https://restaurantezodiacbenidorm.es/wp-content/uploads/2021/02/Cerveza-Poker-en-Benidorm-450x450.jpg",  qty=10),
    Beer(beer_id=2, name="Club Colombia", price=15.0, image="https://jotajotafoods.com/wp-content/uploads/2022/05/CER00005.jpg", qty=10),
    Beer(beer_id=3, name="Costeña", price=13.0, image="https://www.univorca.com/wp-content/uploads/2020/07/coste%C3%B1a-cerveza-exportacion-600x600.jpg", qty=10),
    Beer(beer_id=4, name="Andina", price=11.0, image="https://www.monde-selection.com/wp-content/uploads/2020/05/_XT20031.png", qty=10),
    Beer(beer_id=5, name="BBC Rubia", price=14.0, image="https://www.bbccerveceria.com/sites/g/files/seuoyk221/files/2022-07/Lager.png", qty=10),
]

InMeoryOrders = []

@app.get("/beers", response_model=List[Beer])
async def list_beers():
    """
    This endpoint returns a list of beers avaliable in the bar
    """
    return [beer for beer in InMemoryBeers if beer.qty > 0]

# recive order should minus the qty of the beer save in beers list

@app.post("/order", response_model=Order)
async def receive_order(order: OrderSchema):
    beers_to_discount = []
    for beer in order.beers:
        instore_beer = InMemoryBeers[beer.beer_id]
        if beer.qty > instore_beer.qty:
            return JSONResponse(status_code=400, content={"message": f"Only {instore_beer.qty} {instore_beer.name} left"})
        
        add = Beer(beer_id=instore_beer.beer_id,price=instore_beer.price, qty=beer.qty)
        beers_to_discount.append(add)
                
    
    for beer in beers_to_discount:
        InMemoryBeers[beer.beer_id].qty -= beer.qty
    
    order.beers = beers_to_discount
    save_order = Order(order_id=order.order_id, beers=order.beers, orderby=order.orderby)
    InMeoryOrders.append(save_order)
    return JSONResponse(status_code=201, content={"message": "Order received"})

@app.get("/bill", response_model=Bill)
async def get_bill(order_id: int):
    # filter orders by order_id
    instore_orders = [order for order in InMeoryOrders if order.order_id == order_id]
    if len(instore_orders) == 0:
        return JSONResponse(status_code=404, content={"message": "Order not found"})
    # get beer price by beer_id and multiply by qty and sum all
    total = sum(beer.price * beer.qty for order in instore_orders for beer in order.beers)


    return Bill(orders=instore_orders, total=total)

@app.post("/pay")
async def pay_bill(order_id: int,  friend_id: int | None = None, split: int = 1):
    """
    Calculate and pay the bill for a given order or for a specific friend.

    Args:
        order_id (int): The ID of the order.
        friend_id (int, optional): The ID of the friend. Defaults to None.
        split (int, optional): The number of orders to split the bill. Defaults to 1.

    Returns:
        JSONResponse: The response containing the bill information or an error message.
    """
    instore_orders = [order for order in InMeoryOrders if order.order_id == order_id and order.status == "pending"]
    if len(instore_orders) == 0:
        return JSONResponse(status_code=404, content={"message": "Order not found"})
    if friend_id:
        # calculate the bill for that friend
        bill = sum(beer.price * beer.qty for order in instore_orders for beer in order.beers)
        # change the status of the orders to paid of that friend
        for order in InMeoryOrders:
            if order.orderby == friend_id:
                order.status = "paid"
        return JSONResponse(status_code=200, content={"message": f"Bill for friend {friend_id} is {bill}"})
    else:
        num_orders = len(instore_orders) // split
        # take the number of orders equal to num_orders result, calculate the bill and change the status of the orders to paid
        total = 0
        for i in range(num_orders):
            order = instore_orders[i]
            total += sum(beer.price * beer.qty for beer in order.beers)
            for in_memory_order in InMeoryOrders:
                if in_memory_order.order_id == order.order_id:
                    in_memory_order.status = "paid"
        
     
        return JSONResponse(status_code=200, content={"message": f"total bill is {total}"})

