from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# -------------------------
# 1. Root endpoint
# -------------------------
@app.get("/")
def get_home():
    return {"message": "Welcome to our E-commerce API"}

# -------------------------
# 2. Products
# -------------------------
products = [
    {"id": 1, "name": "Laptop", "description": "A powerful laptop", "price": 1200, "image": "laptop.jpg"},
    {"id": 2, "name": "Phone", "description": "A smartphone", "price": 800, "image": "phone.jpg"},
    {"id": 3, "name": "Headphones", "description": "Noise-cancelling headphones", "price": 150, "image": "headphones.jpg"},
    {"id": 4, "name": "Smartwatch", "description": "A stylish smartwatch", "price": 200, "image": "smartwatch.jpg"},
]

@app.get("/products")
def get_products():
    return {"products": products}

@app.get("/products/{id}")
def get_product(id: int):
    for product in products:
        if product["id"] == id:
            return product
    return {"error": "Product not found"}

# -------------------------
# 3. Users
# -------------------------
users = []

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

@app.post("/register")
def register(user: User):
    # check if user already exists
    for u in users:
        if u["username"] == user.username or u["email"] == user.email:
            return {"error": "User already exists"}
    users.append(user.dict())
    return {"message": "User registered successfully"}

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginData):
    for u in users:
        if (u["username"] == data.username or u["email"] == data.username) and u["password"] == data.password:
            return {"message": "Login successful"}
    return {"error": "Invalid credentials"}

# -------------------------
# 4. Cart
# -------------------------
carts = {}  # {user_id: [ {product_id, quantity}, … ] }

class CartItem(BaseModel):
    user_id: int
    product_id: int
    quantity: int

@app.post("/cart")
def add_to_cart(item: CartItem):
    if item.user_id not in carts:
        carts[item.user_id] = []
    carts[item.user_id].append({"product_id": item.product_id, "quantity": item.quantity})
    return {"message": "Item added to cart", "cart": carts[item.user_id]}

@app.get("/cart/{user_id}")
def get_cart(user_id: int):
    return {"cart": carts.get(user_id, [])}

# -------------------------
# 5. Checkout
# -------------------------
@app.post("/checkout/{user_id}")
def checkout(user_id: int):
    if user_id not in carts or not carts[user_id]:
        return {"error": "Cart is empty"}

    cart_items = carts[user_id]
    order_summary = []
    total = 0

    for item in cart_items:
        for product in products:
            if product["id"] == item["product_id"]:
                subtotal = product["price"] * item["quantity"]
                total += subtotal
                order_summary.append({
                    "product": product["name"],
                    "quantity": item["quantity"],
                    "price": product["price"],
                    "subtotal": subtotal
                })

    return {
        "user_id": user_id,
        "order_summary": order_summary,
        "total": total
    }
