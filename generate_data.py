# generate_data.py
"""
Generate synthetic e-commerce CSV files:
- users.csv
- products.csv
- orders.csv
- order_items.csv
- reviews.csv

Run: python generate_data.py
Requires: pandas, faker
"""

from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()

def make_users(n=50):
    rows = []
    for i in range(1, n+1):
        rows.append({
            "user_id": i,
            "email": fake.unique.email(),
            "name": fake.name(),
            "signup_date": fake.date_between(start_date='-2y', end_date='today').isoformat(),
            "country": fake.country()
        })
    return pd.DataFrame(rows)

def make_products(n=50):
    rows = []
    categories = ["clothing", "electronics", "home", "books", "toys"]
    for i in range(1, n+1):
        rows.append({
            "product_id": i,
            "name": f"{fake.word().capitalize()} {fake.word().capitalize()}",
            "category": random.choice(categories),
            "price": round(random.uniform(5, 500), 2),
            "in_stock": random.randint(0, 500)
        })
    return pd.DataFrame(rows)

def make_orders(n=200, user_count=50):
    rows = []
    start = datetime.now() - timedelta(days=365)
    for i in range(1, n+1):
        user_id = random.randint(1, user_count)
        order_date = start + timedelta(days=random.randint(0, 365))
        rows.append({
            "order_id": i,
            "user_id": user_id,
            "order_date": order_date.date().isoformat(),
            "status": random.choice(["completed", "pending", "cancelled", "shipped"]),
            "total_amount": 0.0
        })
    return pd.DataFrame(rows)

def make_order_items(orders_df, product_count=50, max_items_per_order=5):
    rows = []
    item_id = 1
    for _, order in orders_df.iterrows():
        num_items = random.randint(1, max_items_per_order)
        for _ in range(num_items):
            product_id = random.randint(1, product_count)
            qty = random.randint(1, 5)
            unit_price = round(random.uniform(5, 500), 2)
            rows.append({
                "item_id": item_id,
                "order_id": order['order_id'],
                "product_id": product_id,
                "quantity": qty,
                "unit_price": unit_price,
                "line_total": round(qty * unit_price, 2)
            })
            item_id += 1
    return pd.DataFrame(rows)

def make_reviews(n=150, user_count=50, product_count=50):
    rows = []
    for i in range(1, n+1):
        rows.append({
            "review_id": i,
            "product_id": random.randint(1, product_count),
            "user_id": random.randint(1, user_count),
            "rating": random.randint(1, 5),
            "review_text": fake.sentence(nb_words=12),
            "created_at": fake.date_between(start_date='-2y', end_date='today').isoformat()
        })
    return pd.DataFrame(rows)

def main():
    users = make_users(n=50)
    products = make_products(n=50)
    orders = make_orders(n=200, user_count=users.shape[0])
    order_items = make_order_items(orders, product_count=products.shape[0])
    # compute order totals
    order_totals = order_items.groupby("order_id")["line_total"].sum().reset_index()
    orders = orders.merge(order_totals, on="order_id", how="left").rename(columns={"line_total":"total_amount"})
    orders["total_amount"] = orders["total_amount"].fillna(0).round(2)

    reviews = make_reviews(n=150, user_count=users.shape[0], product_count=products.shape[0])

    users.to_csv("users.csv", index=False)
    products.to_csv("products.csv", index=False)
    orders.to_csv("orders.csv", index=False)
    order_items.to_csv("order_items.csv", index=False)
    reviews.to_csv("reviews.csv", index=False)

    print("Generated CSVs: users.csv, products.csv, orders.csv, order_items.csv, reviews.csv")

if __name__ == "__main__":
    main()
