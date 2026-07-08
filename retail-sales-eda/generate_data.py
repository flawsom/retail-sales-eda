"""
generate_data.py
Generates a realistic synthetic retail sales transaction dataset with
real-world messiness (missing values, duplicates, outliers, inconsistent
casing) so it can be used for a genuine data-cleaning + EDA exercise.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

N = 12000
start_date = pd.Timestamp("2023-01-01")
end_date = pd.Timestamp("2024-12-31")
date_range_days = (end_date - start_date).days

categories = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Smartwatch", "Bluetooth Speaker"],
    "Apparel": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Cap"],
    "Home & Kitchen": ["Blender", "Cookware Set", "Vacuum Cleaner", "Air Purifier", "Table Lamp"],
    "Groceries": ["Rice 5kg", "Cooking Oil 1L", "Snack Pack", "Tea Box", "Coffee Jar"],
    "Beauty": ["Face Wash", "Shampoo", "Sunscreen", "Lipstick", "Perfume"],
}
regions = ["East", "West", "North", "South"]
channels = ["Online", "In-Store", "Marketplace"]
payment_methods = ["Credit Card", "UPI", "Cash", "Debit Card", "Net Banking"]

rows = []
for i in range(N):
    cat = rng.choice(list(categories.keys()), p=[0.28, 0.22, 0.18, 0.20, 0.12])
    product = rng.choice(categories[cat])
    order_date = start_date + pd.Timedelta(days=int(rng.integers(0, date_range_days)))

    # seasonal boost for Electronics/Apparel in Oct-Dec, Groceries flat, Beauty slight boost in summer
    month = order_date.month
    seasonal_mult = 1.0
    if cat in ("Electronics", "Apparel") and month in (10, 11, 12):
        seasonal_mult = 1.6
    if cat == "Beauty" and month in (4, 5, 6):
        seasonal_mult = 1.3

    base_price = {
        "Electronics": rng.uniform(800, 45000),
        "Apparel": rng.uniform(299, 3500),
        "Home & Kitchen": rng.uniform(499, 12000),
        "Groceries": rng.uniform(40, 900),
        "Beauty": rng.uniform(120, 2500),
    }[cat]

    unit_price = round(base_price, 2)
    quantity = int(rng.choice([1, 1, 1, 2, 2, 3, 4], p=[0.35, 0.2, 0.15, 0.15, 0.07, 0.05, 0.03]))
    discount_pct = round(float(rng.choice([0, 0, 0, 5, 10, 15, 20, 25], p=[0.35,0.15,0.1,0.15,0.1,0.08,0.05,0.02])), 2)

    gross = unit_price * quantity * seasonal_mult
    discount_amt = gross * (discount_pct / 100)
    net_sales = gross - discount_amt
    cost_ratio = rng.uniform(0.55, 0.8)
    cost = gross * cost_ratio
    profit = net_sales - cost

    region = rng.choice(regions)
    channel = rng.choice(channels, p=[0.55, 0.30, 0.15])
    payment = rng.choice(payment_methods)

    rows.append({
        "OrderID": 100000 + i,
        "OrderDate": order_date,
        "Category": cat,
        "Product": product,
        "Region": region,
        "Channel": channel,
        "PaymentMethod": payment,
        "Quantity": quantity,
        "UnitPrice": round(unit_price, 2),
        "DiscountPct": discount_pct,
        "GrossSales": round(gross, 2),
        "NetSales": round(net_sales, 2),
        "Profit": round(profit, 2),
    })

df = pd.DataFrame(rows)

# ---- inject realistic messiness ----
# 1. Missing values in Region and PaymentMethod
missing_idx = rng.choice(df.index, size=int(N * 0.035), replace=False)
df.loc[missing_idx, "Region"] = np.nan
missing_idx2 = rng.choice(df.index, size=int(N * 0.02), replace=False)
df.loc[missing_idx2, "PaymentMethod"] = np.nan

# 2. Inconsistent category casing / whitespace (real-world data entry issues)
messy_idx = rng.choice(df.index, size=int(N * 0.04), replace=False)
df.loc[messy_idx, "Category"] = df.loc[messy_idx, "Category"].str.lower()
messy_idx2 = rng.choice(df.index, size=int(N * 0.02), replace=False)
df.loc[messy_idx2, "Category"] = " " + df.loc[messy_idx2, "Category"].astype(str) + " "

# 3. Duplicate rows
dupes = df.sample(n=int(N * 0.015), random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

# 4. A few extreme outliers in NetSales (data entry errors, e.g. misplaced decimal)
outlier_idx = rng.choice(df.index, size=12, replace=False)
df.loc[outlier_idx, "NetSales"] = df.loc[outlier_idx, "NetSales"] * 50

# 5. A few negative Quantity (returns logged incorrectly)
neg_idx = rng.choice(df.index, size=8, replace=False)
df.loc[neg_idx, "Quantity"] = -df.loc[neg_idx, "Quantity"]

df = df.sample(frac=1, random_state=7).reset_index(drop=True)
df.to_csv("retail_sales_raw.csv", index=False)
print(f"Generated {len(df)} rows -> retail_sales_raw.csv")
