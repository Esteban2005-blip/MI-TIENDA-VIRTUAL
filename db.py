import sqlite3
import os
from typing import List, Optional

from inventory import Product

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DB_DIR, "inventory.db")


def get_conn():
    os.makedirs(DB_DIR, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def insert_product(product: Product) -> None:
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO products (id, name, quantity, price, description) VALUES (?,?,?,?,?)",
        (product.id, product.name, product.quantity, product.price, product.description),
    )
    conn.commit()
    conn.close()


def update_product(product: Product) -> None:
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE products SET name=?, quantity=?, price=?, description=? WHERE id=?",
        (product.name, product.quantity, product.price, product.description, product.id),
    )
    conn.commit()
    conn.close()


def delete_product(product_id: int) -> None:
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()


def get_product(product_id: int) -> Optional[Product]:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, quantity, price, description FROM products WHERE id=?", (product_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return Product(*row)
    return None


def find_products_by_name(name: str) -> List[Product]:
    conn = get_conn()
    c = conn.cursor()
    like = f"%{name}%"
    c.execute("SELECT id, name, quantity, price, description FROM products WHERE name LIKE ?", (like,))
    rows = c.fetchall()
    conn.close()
    return [Product(*r) for r in rows]


def list_products() -> List[Product]:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, quantity, price, description FROM products ORDER BY name")
    rows = c.fetchall()
    conn.close()
    return [Product(*r) for r in rows]
