-- analysis_queries.sql
-- A set of portfolio-worthy analytical queries against the `sales` table.
-- Run against ../data/sales.db, e.g.:
--     sqlite3 ../data/sales.db < analysis_queries.sql
-- or open the .db file in DB Browser for SQLite / any SQL client.

-- 1. Overall KPIs
SELECT
    COUNT(DISTINCT order_id)               AS total_orders,
    COUNT(DISTINCT customer_id)             AS unique_customers,
    ROUND(SUM(net_sales), 2)                AS total_revenue,
    ROUND(AVG(net_sales), 2)                AS avg_order_value,
    ROUND(SUM(discount_amount), 2)          AS total_discounts_given
FROM sales;

-- 2. Monthly revenue trend + month-over-month growth %
WITH monthly AS (
    SELECT
        order_year,
        order_month,
        order_month_name,
        ROUND(SUM(net_sales), 2) AS revenue
    FROM sales
    GROUP BY order_year, order_month
)
SELECT
    order_year,
    order_month_name,
    revenue,
    ROUND(
        100.0 * (revenue - LAG(revenue) OVER (ORDER BY order_year, order_month))
        / NULLIF(LAG(revenue) OVER (ORDER BY order_year, order_month), 0),
    2) AS mom_growth_pct
FROM monthly
ORDER BY order_year, order_month;

-- 3. Top 10 products by revenue
SELECT
    product,
    category,
    SUM(quantity)              AS units_sold,
    ROUND(SUM(net_sales), 2)   AS revenue
FROM sales
GROUP BY product, category
ORDER BY revenue DESC
LIMIT 10;

-- 4. Revenue and average order value by region
SELECT
    region,
    COUNT(DISTINCT order_id)   AS orders,
    ROUND(SUM(net_sales), 2)   AS revenue,
    ROUND(AVG(net_sales), 2)   AS avg_order_value
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- 5. Customer segmentation: revenue contribution and order frequency
SELECT
    customer_segment,
    COUNT(DISTINCT customer_id) AS customers,
    COUNT(DISTINCT order_id)    AS orders,
    ROUND(SUM(net_sales), 2)    AS revenue,
    ROUND(SUM(net_sales) * 1.0 / COUNT(DISTINCT customer_id), 2) AS revenue_per_customer
FROM sales
GROUP BY customer_segment
ORDER BY revenue DESC;

-- 6. Top 10 customers by lifetime value (RFM-style building block)
SELECT
    customer_id,
    COUNT(DISTINCT order_id)    AS total_orders,
    ROUND(SUM(net_sales), 2)    AS lifetime_value,
    MAX(order_date)             AS last_order_date
FROM sales
GROUP BY customer_id
ORDER BY lifetime_value DESC
LIMIT 10;

-- 7. Payment method popularity vs. average order value
SELECT
    payment_method,
    COUNT(DISTINCT order_id)  AS orders,
    ROUND(AVG(net_sales), 2)  AS avg_order_value
FROM sales
GROUP BY payment_method
ORDER BY orders DESC;

-- 8. Category performance with discount impact
SELECT
    category,
    ROUND(SUM(gross_sales), 2)                              AS gross_revenue,
    ROUND(SUM(discount_amount), 2)                          AS total_discount,
    ROUND(SUM(net_sales), 2)                                AS net_revenue,
    ROUND(100.0 * SUM(discount_amount) / NULLIF(SUM(gross_sales), 0), 2) AS discount_rate_pct
FROM sales
GROUP BY category
ORDER BY net_revenue DESC;

-- 9. Quarter-over-quarter revenue comparison
SELECT
    order_year,
    order_quarter,
    ROUND(SUM(net_sales), 2) AS revenue
FROM sales
GROUP BY order_year, order_quarter
ORDER BY order_year, order_quarter;

-- 10. Cities ranked within each region (window function)
SELECT region, city, revenue, city_rank
FROM (
    SELECT
        region,
        city,
        ROUND(SUM(net_sales), 2) AS revenue,
        RANK() OVER (PARTITION BY region ORDER BY SUM(net_sales) DESC) AS city_rank
    FROM sales
    GROUP BY region, city
)
WHERE city_rank <= 3
ORDER BY region, city_rank;
