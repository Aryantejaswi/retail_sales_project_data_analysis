"""
eda_analysis.py
----------------
Exploratory Data Analysis on the cleaned sales data.
Reads straight from the SQLite database (sales.db) using SQL queries,
then visualizes results with matplotlib/seaborn. Charts are saved to
../outputs/ for inclusion in the portfolio write-up / README.

Run:
    python eda_analysis.py
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
DB_PATH = "../data/sales.db"
OUT_DIR = "../outputs"

conn = sqlite3.connect(DB_PATH)

# 1. Monthly revenue trend
monthly = pd.read_sql("""
    SELECT order_year, order_month, order_month_name,
           ROUND(SUM(net_sales), 2) AS revenue
    FROM sales
    GROUP BY order_year, order_month
    ORDER BY order_year, order_month
""", conn)
monthly["period"] = monthly["order_month_name"] + " " + monthly["order_year"].astype(str)

plt.figure(figsize=(12, 5))
sns.lineplot(data=monthly, x="period", y="revenue", marker="o", sort=False)
plt.xticks(rotation=60)
plt.title("Monthly Net Revenue Trend")
plt.ylabel("Net Revenue (₹)")
plt.xlabel("")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/monthly_revenue_trend.png", dpi=150)
plt.close()

# 2. Revenue by category
by_category = pd.read_sql("""
    SELECT category, ROUND(SUM(net_sales), 2) AS revenue
    FROM sales
    GROUP BY category
    ORDER BY revenue DESC
""", conn)

plt.figure(figsize=(8, 5))
sns.barplot(data=by_category, x="revenue", y="category", palette="viridis")
plt.title("Net Revenue by Category")
plt.xlabel("Net Revenue (₹)")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/revenue_by_category.png", dpi=150)
plt.close()

# 3. Revenue by region
by_region = pd.read_sql("""
    SELECT region, ROUND(SUM(net_sales), 2) AS revenue
    FROM sales
    GROUP BY region
    ORDER BY revenue DESC
""", conn)

plt.figure(figsize=(7, 5))
sns.barplot(data=by_region, x="region", y="revenue", palette="mako")
plt.title("Net Revenue by Region")
plt.ylabel("Net Revenue (₹)")
plt.xlabel("")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/revenue_by_region.png", dpi=150)
plt.close()

# 4. Customer segment contribution
by_segment = pd.read_sql("""
    SELECT customer_segment, ROUND(SUM(net_sales), 2) AS revenue
    FROM sales
    GROUP BY customer_segment
    ORDER BY revenue DESC
""", conn)

plt.figure(figsize=(6, 6))
plt.pie(by_segment["revenue"], labels=by_segment["customer_segment"],
        autopct="%1.1f%%", startangle=90,
        colors=sns.color_palette("pastel"))
plt.title("Revenue Share by Customer Segment")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/revenue_by_segment.png", dpi=150)
plt.close()

# 5. Top 10 products by revenue
top_products = pd.read_sql("""
    SELECT product, ROUND(SUM(net_sales), 2) AS revenue
    FROM sales
    GROUP BY product
    ORDER BY revenue DESC
    LIMIT 10
""", conn)

plt.figure(figsize=(9, 5))
sns.barplot(data=top_products, x="revenue", y="product", palette="flare")
plt.title("Top 10 Products by Net Revenue")
plt.xlabel("Net Revenue (₹)")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/top_10_products.png", dpi=150)
plt.close()

conn.close()
print("EDA complete. 5 charts saved to ../outputs/")
