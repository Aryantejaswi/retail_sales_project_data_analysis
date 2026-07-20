"""
generate_data.py
-----------------
Generates a synthetic retail sales dataset for the portfolio project.
Creates realistic (but fake) transactional data with intentional
data-quality issues (nulls, duplicates, inconsistent text) so the
ETL/cleaning step has real work to do.

Run:
    python generate_data.py

Output:
    ../data/raw_sales.csv
"""

import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

N_ROWS = 12000

CATEGORIES = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Tablet", "Smartwatch"],
    "Home & Kitchen": ["Blender", "Coffee Maker", "Cookware Set", "Air Fryer", "Vacuum"],
    "Apparel": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Dress"],
    "Beauty": ["Shampoo", "Perfume", "Skincare Set", "Makeup Kit", "Hair Dryer"],
    "Sports": ["Yoga Mat", "Dumbbells", "Running Shoes", "Bicycle", "Tent"],
}

REGIONS = {
    "North": ["Delhi", "Chandigarh", "Jaipur"],
    "South": ["Bangalore", "Chennai", "Hyderabad"],
    "East": ["Kolkata", "Bhubaneswar", "Guwahati"],
    "West": ["Mumbai", "Pune", "Ahmedabad"],
}

PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery"]
CUSTOMER_SEGMENTS = ["New", "Returning", "VIP"]

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
date_range_days = (end_date - start_date).days


def random_date():
    return start_date + timedelta(days=random.randint(0, date_range_days))


rows = []
for i in range(1, N_ROWS + 1):
    category = random.choice(list(CATEGORIES.keys()))
    product = random.choice(CATEGORIES[category])
    region = random.choice(list(REGIONS.keys()))
    city = random.choice(REGIONS[region])

    base_price = {
        "Electronics": np.random.uniform(1500, 60000),
        "Home & Kitchen": np.random.uniform(800, 8000),
        "Apparel": np.random.uniform(300, 3500),
        "Beauty": np.random.uniform(150, 2500),
        "Sports": np.random.uniform(400, 15000),
    }[category]

    unit_price = round(base_price, 2)
    quantity = random.randint(1, 5)
    discount_pct = random.choice([0, 0, 0, 5, 10, 15, 20, 25])
    discount_amt = round(unit_price * quantity * discount_pct / 100, 2)
    gross_sales = round(unit_price * quantity, 2)
    net_sales = round(gross_sales - discount_amt, 2)

    order_date = random_date()

    row = {
        "order_id": f"ORD{100000 + i}",
        "order_date": order_date.strftime("%Y-%m-%d"),
        "customer_id": f"CUST{random.randint(1000, 3500)}",
        "customer_segment": random.choice(CUSTOMER_SEGMENTS),
        "region": region,
        "city": city,
        "category": category,
        "product": product,
        "unit_price": unit_price,
        "quantity": quantity,
        "discount_pct": discount_pct,
        "discount_amount": discount_amt,
        "gross_sales": gross_sales,
        "net_sales": net_sales,
        "payment_method": random.choice(PAYMENT_METHODS),
    }
    rows.append(row)

df = pd.DataFrame(rows)

# ---- Inject realistic data-quality issues on purpose ----

# 1. Random nulls in customer_segment and payment_method
null_idx = df.sample(frac=0.03, random_state=1).index
df.loc[null_idx, "customer_segment"] = np.nan

null_idx2 = df.sample(frac=0.02, random_state=2).index
df.loc[null_idx2, "payment_method"] = np.nan

# 2. Inconsistent text casing/whitespace in region/city
messy_idx = df.sample(frac=0.05, random_state=3).index
df.loc[messy_idx, "region"] = df.loc[messy_idx, "region"].str.lower()

messy_idx2 = df.sample(frac=0.05, random_state=4).index
df.loc[messy_idx2, "city"] = " " + df.loc[messy_idx2, "city"] + "  "

# 3. Duplicate rows
dup_rows = df.sample(frac=0.01, random_state=5)
df = pd.concat([df, dup_rows], ignore_index=True)

# 4. A few negative/invalid quantities (data entry errors)
err_idx = df.sample(frac=0.005, random_state=6).index
df.loc[err_idx, "quantity"] = -1

# Shuffle rows
df = df.sample(frac=1, random_state=7).reset_index(drop=True)

df.to_csv("../data/raw_sales.csv", index=False)
print(f"Generated {len(df)} rows -> ../data/raw_sales.csv")
