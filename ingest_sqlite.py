# ingest_sqlite.py
"""
Ingest CSV files into SQLite database ecom.db
Run: python ingest_sqlite.py
Requires: pandas, sqlalchemy
"""

import pandas as pd
from sqlalchemy import create_engine

DB_FILE = "ecom.db"
engine = create_engine(f"sqlite:///{DB_FILE}")

def to_sql_from_csv(csv_file, table_name):
    print(f"Loading {csv_file} -> {table_name}")
    df = pd.read_csv(csv_file)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into {table_name}")

def main():
    to_sql_from_csv("users.csv", "users")
    to_sql_from_csv("products.csv", "products")
    to_sql_from_csv("orders.csv", "orders")
    to_sql_from_csv("order_items.csv", "order_items")
    to_sql_from_csv("reviews.csv", "reviews")
    print("All tables loaded into", DB_FILE)

if __name__ == "__main__":
    main()
