# 🛒 E-Commerce API

This is a simple **E-commerce API** built with FastAPI the using **products, users, cart, and checkout** features.

---
## 📸 API Preview

![API Screenshot](https://i.postimg.cc/zXYCQg2D/screencapture-127-0-0-1-8000-docs-2025-09-05-12-23-24.png)

*(The image above shows the FastAPI interactive Swagger docs.)*

---

## 🚀 Features

- **Products**
  - `GET /products` → Get all products
  - `GET /products/{id}` → Get product details by ID

- **Users**
  - `POST /register` → Register a new user
  - `POST /login` → Login with username/email + password

- **Cart**
  - `POST /cart` → Add product(s) to user’s cart
  - `GET /cart/{user_id}` → View user’s cart

- **Checkout**
  - `POST /checkout/{user_id}` → Get an order summary with total cost

