CREATE TABLE IF NOT EXISTS products (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS warehouses (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS stock_balances (
    product_id BIGINT NOT NULL REFERENCES products(id),
    warehouse_id BIGINT NOT NULL REFERENCES warehouses(id),
    physical_quantity INTEGER NOT NULL DEFAULT 0 CHECK (physical_quantity >= 0),
    fbs_reserved INTEGER NOT NULL DEFAULT 0 CHECK (fbs_reserved >= 0),
    PRIMARY KEY (product_id, warehouse_id),
    CHECK (fbs_reserved <= physical_quantity)
);

CREATE TABLE IF NOT EXISTS stock_operations (
    id UUID PRIMARY KEY,
    operation_type TEXT NOT NULL,
    product_id BIGINT NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    source_warehouse_id BIGINT REFERENCES warehouses(id),
    destination_warehouse_id BIGINT REFERENCES warehouses(id),
    destination TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
