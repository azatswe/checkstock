"""Load the original CheckStock demo data into an empty database."""

import os

import psycopg


PRODUCTS = (
    ("SKU-101", "Органайзер"),
    ("SKU-102", "Контейнер"),
    ("SKU-103", "Корзина"),
)
WAREHOUSES = ("Север", "Юг")
INITIAL_STOCK = {
    ("SKU-101", "Север"): 10,
    ("SKU-101", "Юг"): 6,
    ("SKU-102", "Север"): 5,
    ("SKU-102", "Юг"): 0,
    ("SKU-103", "Север"): 0,
    ("SKU-103", "Юг"): 4,
}


def seed_database() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise SystemExit("Не задан DATABASE_URL. Скопируйте .env.example в .env и экспортируйте настройки.")

    try:
        with psycopg.connect(database_url) as connection:
            has_existing_data = connection.execute(
                """
                SELECT
                    EXISTS (SELECT 1 FROM products)
                    OR EXISTS (SELECT 1 FROM warehouses)
                    OR EXISTS (SELECT 1 FROM stock_balances)
                    OR EXISTS (SELECT 1 FROM stock_operations)
                """
            ).fetchone()[0]

            if has_existing_data:
                print("Начальные данные не загружены: база уже содержит данные, остатки не изменены.")
                return

            product_ids = {}
            for sku, name in PRODUCTS:
                product_ids[sku] = connection.execute(
                    "INSERT INTO products (sku, name) VALUES (%s, %s) RETURNING id",
                    (sku, name),
                ).fetchone()[0]

            warehouse_ids = {}
            for name in WAREHOUSES:
                warehouse_ids[name] = connection.execute(
                    "INSERT INTO warehouses (name) VALUES (%s) RETURNING id",
                    (name,),
                ).fetchone()[0]

            for (sku, warehouse_name), quantity in INITIAL_STOCK.items():
                connection.execute(
                    """
                    INSERT INTO stock_balances (product_id, warehouse_id, physical_quantity)
                    VALUES (%s, %s, %s)
                    """,
                    (product_ids[sku], warehouse_ids[warehouse_name], quantity),
                )
    except psycopg.Error as error:
        raise SystemExit(f"Не удалось загрузить тестовые данные: {error}") from None

    print("Тестовые товары, ФФ и начальные остатки загружены.")


if __name__ == "__main__":
    seed_database()
