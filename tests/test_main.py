from fastapi.testclient import TestClient

from beer_friends.main import InMemoryBeers, app
from beer_friends.schemas.beer_schema import BeerSchema
from beer_friends.schemas.order_schema import OrderSchema

client = TestClient(app)

def test_receive_order():
    # Test case 1: Sufficient quantity of beers available
    order1 = OrderSchema(order_id=23, orderby=1045, beers=[BeerSchema(beer_id=1, qty=2)])
    response = client.post("/order", json=order1.model_dump())
    assert response.status_code == 201
    assert response.json() == {"message": "Order received"}

    # Test case 2: Insufficient quantity of beers available
    order2 = OrderSchema(order_id=23, orderby=1045, beers=[BeerSchema(beer_id=2, qty=30)])
    result2 = client.post("/order", json=order2.model_dump())
    assert result2.status_code == 400

def test_get_bill():
    # Test case 1: Order found
    orders = [
        OrderSchema(order_id=23, orderby=1045, beers=[BeerSchema(beer_id=1, qty=2)]).model_dump(),
        OrderSchema(order_id=23, orderby=1045, beers=[BeerSchema(beer_id=2, qty=3)]).model_dump()
    ]
    client.post("/order", json=orders[1])
    response = client.get("/bill?order_id=23")
    assert response.status_code == 200
    assert response.json().get("total") == 69.0

    # Test case 2: Order not found
    response = client.get("/bill?order_id=24")
    assert response.status_code == 404
    assert response.json() == {"message": "Order not found"}

def test_pay_bill():
    # Test case 1: Order found
    orders = [
        OrderSchema(order_id=23, orderby=1045, beers=[BeerSchema(beer_id=1, qty=2)]).model_dump(),
        OrderSchema(order_id=23, orderby=1045, beers=[BeerSchema(beer_id=2, qty=3)]).model_dump()
    ]
    client.post("/order", json=orders[1])
    response = client.post("/pay?order_id=23&friend_id=1045")
    assert response.status_code == 200
    assert response.json() == {"message": "Bill for friend 1045 is 114.0"}

    # Test case 2: Order not found
    response = client.post("/pay?order_id=24&friend_id=1045")
    assert response.status_code == 404
    assert response.json() == {"message": "Order not found"}

    # Test case 3: Order not found, friend_id not set
    response = client.post("/pay?order_id=40")
    assert response.status_code == 404
    assert response.json() == {"message": "Order not found"}

     # Test case 4: Order found, friend_id not set
    order1 = OrderSchema(order_id=50, orderby=1046, beers=[BeerSchema(beer_id=1, qty=2)])
    client.post("/order", json=order1.model_dump())
    response = client.post("/pay?order_id=50")
    beers_price = 0
    for beer in order1.beers:
        beer_from_memory = InMemoryBeers[beer.beer_id]
        beers_price += beer_from_memory.price * beer.qty
    assert response.status_code == 200
    assert response.json() == {"message": f"total bill is {beers_price}"}
