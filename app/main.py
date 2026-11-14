import os
from pathlib import Path

import psycopg
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse


app = FastAPI(title="CheckStock")
STATIC_DIR = Path(__file__).parent / "static"


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/stock", tags=["stock"])
def get_stock() -> dict[str, list[dict[str, object]]]:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise HTTPException(status_code=503, detail="База данных не настроена.")

    query = """
        SELECT
            p.sku,
            p.name AS product_name,
            w.name AS warehouse_name,
            COALESCE(b.physical_quantity, 0) AS physical_quantity,
            COALESCE(b.fbs_reserved, 0) AS fbs_reserved,
            COALESCE(b.physical_quantity, 0) - COALESCE(b.fbs_reserved, 0) AS available
        FROM products AS p
        CROSS JOIN warehouses AS w
        LEFT JOIN stock_balances AS b
            ON b.product_id = p.id AND b.warehouse_id = w.id
        WHERE w.is_active = TRUE
        ORDER BY p.sku, w.name
    """

    try:
        with psycopg.connect(database_url) as connection:
            rows = connection.execute(query).fetchall()
    except psycopg.Error:
        raise HTTPException(status_code=503, detail="Не удалось получить остатки из базы данных.") from None

    return {
        "items": [
            {
                "sku": row[0],
                "product_name": row[1],
                "warehouse_name": row[2],
                "physical_quantity": row[3],
                "fbs_reserved": row[4],
                "available": row[5],
            }
            for row in rows
        ]
    }
