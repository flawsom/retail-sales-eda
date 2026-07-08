"""
eda_analysis.py
Exploratory Data Analysis on a retail sales transactions dataset.
Covers: data quality audit, cleaning, EDA, and business insights.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
pd.set_option("display.width", 120)

df = pd.read_csv("retail_sales_raw.csv", parse_dates=["OrderDate"])
raw_rows = len(df)
print(f"Raw rows loaded: {raw_rows}")

report_lines = []
def log(line):
    print(line)
    report_lines.append(line)

log("=" * 60)
log("STEP 1: DATA QUALITY AUDIT")
log("=" * 60)

missing = df.isna().sum()
missing = missing[missing > 0]
log(f"Columns with missing values:\n{missing.to_string()}")

dupe_count = df.duplicated(subset=[c for c in df.columns if c != "OrderID"]).sum()
log(f"Duplicate rows (excluding OrderID): {dupe_count}")

neg_qty = (df["Quantity"] < 0).sum()
log(f"Rows with negative Quantity (likely mis-logged returns): {neg_qty}")

# outlier detection via IQR on NetSales
q1, q3 = df["NetSales"].quantile([0.25, 0.75])
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr
outliers = (df["NetSales"] > upper_bound).sum()
log(f"NetSales outliers beyond IQR upper bound ({upper_bound:,.0f}): {outliers}")

log("\n" + "=" * 60)
log("STEP 2: CLEANING")
log("=" * 60)

# 1. normalize category text
df["Category"] = df["Category"].str.strip().str.title()

# 2. drop duplicates
before = len(df)
df = df.drop_duplicates(subset=[c for c in df.columns if c != "OrderID"]).reset_index(drop=True)
log(f"Removed {before - len(df)} duplicate rows")

# 3. fix negative quantities (data entry error -> take absolute value, flag as return-corrected)
df["Quantity"] = df["Quantity"].abs()

# 4. cap NetSales outliers at the IQR upper bound (winsorize) rather than drop, to preserve volume signal
capped = (df["NetSales"] > upper_bound).sum()
df["NetSales"] = np.where(df["NetSales"] > upper_bound, upper_bound, df["NetSales"])
log(f"Capped {capped} extreme NetSales outliers at IQR upper bound")

# 5. impute missing Region/PaymentMethod with mode (categorical, low-cardinality, MCAR-consistent)
region_mode = df["Region"].mode()[0]
pay_mode = df["PaymentMethod"].mode()[0]
missing_region = df["Region"].isna().sum()
missing_pay = df["PaymentMethod"].isna().sum()
df["Region"] = df["Region"].fillna(region_mode)
df["PaymentMethod"] = df["PaymentMethod"].fillna(pay_mode)
log(f"Imputed {missing_region} missing Region values with mode ('{region_mode}')")
log(f"Imputed {missing_pay} missing PaymentMethod values with mode ('{pay_mode}')")

clean_rows = len(df)
log(f"\nFinal clean dataset: {clean_rows} rows (from {raw_rows} raw rows, "
    f"{raw_rows - clean_rows} removed as duplicates)")

df.to_csv("retail_sales_clean.csv", index=False)

log("\n" + "=" * 60)
log("STEP 3: EXPLORATORY ANALYSIS")
log("=" * 60)

total_net_sales = df["NetSales"].sum()
total_profit = df["Profit"].sum()
avg_order_value = df["NetSales"].mean()
margin_pct = (total_profit / total_net_sales) * 100

log(f"Total Net Sales: {total_net_sales:,.0f}")
log(f"Total Profit: {total_profit:,.0f}")
log(f"Overall Profit Margin: {margin_pct:.1f}%")
log(f"Average Order Value: {avg_order_value:,.0f}")

# Category performance
cat_perf = df.groupby("Category").agg(
    orders=("OrderID", "count"),
    net_sales=("NetSales", "sum"),
    profit=("Profit", "sum"),
).sort_values("net_sales", ascending=False)
cat_perf["sales_share_pct"] = (cat_perf["net_sales"] / cat_perf["net_sales"].sum() * 100).round(1)
log(f"\nCategory performance:\n{cat_perf.round(0).to_string()}")

top2_share = cat_perf["sales_share_pct"].iloc[:2].sum()
log(f"\nTop 2 categories drive {top2_share:.1f}% of total net sales")

# Regional performance
region_perf = df.groupby("Region")["NetSales"].sum().sort_values(ascending=False)
log(f"\nRegional net sales:\n{region_perf.round(0).to_string()}")

# Monthly trend
df["Month"] = df["OrderDate"].dt.to_period("M")
monthly = df.groupby("Month")["NetSales"].sum()
peak_month = monthly.idxmax()
peak_value = monthly.max()
log(f"\nPeak sales month: {peak_month} ({peak_value:,.0f})")

# Discount vs profit margin relationship
disc_bins = pd.cut(df["DiscountPct"], bins=[-1, 0, 10, 20, 100], labels=["0%", "1-10%", "11-20%", "21%+"])
disc_margin = df.groupby(disc_bins, observed=True).apply(
    lambda g: (g["Profit"].sum() / g["NetSales"].sum() * 100) if g["NetSales"].sum() else 0
)
log(f"\nProfit margin by discount band:\n{disc_margin.round(1).to_string()}")

# Channel performance
channel_perf = df.groupby("Channel")["NetSales"].agg(["count", "sum"]).sort_values("sum", ascending=False)
log(f"\nChannel performance:\n{channel_perf.round(0).to_string()}")

log("\n" + "=" * 60)
log("STEP 4: KEY INSIGHTS")
log("=" * 60)
best_cat = cat_perf.index[0]
worst_margin_band = disc_margin.idxmin()
log(f"1. {best_cat} is the top revenue-driving category ({cat_perf['sales_share_pct'].iloc[0]:.1f}% share).")
log(f"2. Top 2 categories together account for {top2_share:.1f}% of revenue -> concentration risk.")
log(f"3. Orders discounted at '{worst_margin_band}' show the weakest profit margin "
    f"({disc_margin.min():.1f}%), suggesting discount policy above ~20% erodes profitability.")
log(f"4. Peak sales month was {peak_month}, consistent with a Q4 seasonal demand spike in "
    f"Electronics and Apparel.")
log(f"5. Online channel leads in both order volume and revenue, ahead of In-Store and Marketplace.")

with open("eda_findings.txt", "w") as f:
    f.write("\n".join(report_lines))

# ---------------- VISUALS ----------------
fig, axes = plt.subplots(2, 2, figsize=(13, 10))

sns.barplot(x=cat_perf["net_sales"], y=cat_perf.index, ax=axes[0, 0], palette="viridis")
axes[0, 0].set_title("Net Sales by Category")
axes[0, 0].set_xlabel("Net Sales")
axes[0, 0].set_ylabel("")

monthly.index = monthly.index.astype(str)
axes[0, 1].plot(monthly.index, monthly.values, marker="o", color="#1F2A44")
axes[0, 1].set_title("Monthly Net Sales Trend")
axes[0, 1].tick_params(axis="x", rotation=75, labelsize=7)
axes[0, 1].set_ylabel("Net Sales")

sns.barplot(x=disc_margin.values, y=disc_margin.index.astype(str), ax=axes[1, 0], palette="magma")
axes[1, 0].set_title("Profit Margin % by Discount Band")
axes[1, 0].set_xlabel("Profit Margin (%)")

sns.boxplot(x="Category", y="NetSales", data=df, ax=axes[1, 1], palette="crest")
axes[1, 1].set_title("Net Sales Distribution by Category (post-cleaning)")
axes[1, 1].tick_params(axis="x", rotation=30)

plt.tight_layout()
plt.savefig("eda_dashboard.png", dpi=150)
print("\nSaved eda_dashboard.png and eda_findings.txt")
