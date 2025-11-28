from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

orders = []

class CustomerRequest(BaseModel):
    customer_name: str
    item: str
    quantity: int
    status: str = "requested"
    order_id: int | None = None

@app.post("/orders")
def create_order(request: CustomerRequest): 
    order = request.model_dump()
    order["order_id"] = len(orders) + 1
    orders.append(order)
    return order

@app.get("/orders")
def get_orders():
    return orders

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="Invalid order ID")

@app.patch("/orders/{order_id}")
def update_order(order_id: int, status: str="processing"):
    order = get_order(order_id)
    order["status"] = status
    return {"updated_order": order}

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            orders.remove(order)
            return {"deleted": order}
    raise HTTPException(status_code=404, detail="Invalid order ID")
