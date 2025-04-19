from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Travel costs per one-way trip
cost_table = {
    'C1': 10,
    'C2': 20,
    'C3': 18
}

# Product availability
center_products = {
    'C1': ['A', 'B', 'C'],
    'C2': ['D', 'E', 'F'],
    'C3': ['G', 'H', 'I']
}

class Order(BaseModel):
    A: int = 0
    B: int = 0
    C: int = 0
    D: int = 0
    E: int = 0
    F: int = 0
    G: int = 0
    H: int = 0
    I: int = 0

def calculate_min_cost(order):
    possible_costs = []

    for start_center in ['C1', 'C2', 'C3']:
        total_cost = 0
        current_location = start_center
        centers_needed = set()

        # Find which centers we need to visit based on order
        for product, quantity in order.items():
            if quantity > 0:
                for center, products in center_products.items():
                    if product in products:
                        centers_needed.add(center)

        visited = set()

        # Simulate visiting each center and dropping to L1
        for center in centers_needed:
            if center != current_location:
                total_cost += abs(cost_table[current_location] - cost_table[center])
                current_location = center
            total_cost += cost_table[center]*2  # Go to L1 and come back

        # Finally, drop remaining items to L1
        if current_location != 'L1':
            total_cost += cost_table[current_location]

        possible_costs.append(total_cost)

    return min(possible_costs)

@app.post("/calculate-cost")
def get_cost(order: Order):
    order_dict = order.dict()
    min_cost = calculate_min_cost(order_dict)
    return {"minimum_cost": min_cost}
