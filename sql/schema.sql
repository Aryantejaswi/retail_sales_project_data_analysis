-- schema.sql
-- Schema for the `sales` table produced by python/etl_load.py.
-- Works as-is on SQLite; minor type tweaks needed for Postgres/MySQL/SQL Server
-- (e.g. TEXT -> VARCHAR, REAL -> DECIMAL, no AUTOINCREMENT syntax differences).

DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    order_id            TEXT PRIMARY KEY,
    order_date           DATE,
    customer_id          TEXT,
    customer_segment     TEXT,
    region                TEXT,
    city                  TEXT,
    category              TEXT,
    product               TEXT,
    unit_price            REAL,
    quantity              INTEGER,
    discount_pct          REAL,
    discount_amount       REAL,
    gross_sales           REAL,
    net_sales             REAL,
    payment_method        TEXT,
    order_year            INTEGER,
    order_month           INTEGER,
    order_month_name      TEXT,
    order_quarter         INTEGER
);

CREATE INDEX idx_sales_date     ON sales(order_date);
CREATE INDEX idx_sales_region   ON sales(region);
CREATE INDEX idx_sales_category ON sales(category);
CREATE INDEX idx_sales_customer ON sales(customer_id);
