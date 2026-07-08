# Superstore Sales EDA — Data Cleaning & Business Insights

An end-to-end exploratory data analysis project on the well-known **Sample Superstore** dataset (a real-world US retail chain's order history, widely used as a standard analytics benchmark dataset). Built with Python (Pandas, NumPy, Matplotlib, Seaborn).

## Dataset
- 9,994 raw order-line records, Jan 2014 – Dec 2017
- 21 fields: order/ship dates, ship mode, customer segment, region, product category/sub-category, sales, quantity, discount, profit
- Source: the standard "Sample Superstore" dataset (commonly distributed with Tableau and used across data-analytics coursework/portfolios)

## What this project demonstrates
- **Data quality auditing:** checked for missing values, duplicate records, and statistical outliers before analysis (this dataset turned out to have no missing values, but is not duplicate- or outlier-free).
- **Data cleaning:** removed duplicate order-line entries, parsed and validated date fields, engineered a shipping-delay feature and a per-line profit-margin feature.
- **Exploratory data analysis:** category/sub-category/regional/segment profitability breakdowns, discount-vs-margin analysis, and time-series trend analysis.
- **Insight generation:** identified which specific product lines and discount tiers were losing the business money — the kind of finding that leads to a pricing or SKU decision.

## Data Quality Findings
| Check | Result |
|---|---|
| Missing values | None found |
| Fully duplicate rows | 0 |
| Duplicate Order ID + Product ID combinations | 8 (removed) |
| Orders sold at a loss (negative profit) | 1,871 (18.7% of all orders) |
| Sales outliers beyond IQR upper bound | 1,167 |

## Key Findings
1. **Technology is the top revenue category** ($835,760, 36.4% of total sales), but **Furniture has the weakest margin** (2.5%) — dragged down by three sub-categories operating at a net loss: **Tables (-9% margin), Bookcases (-3%), and Supplies (-2%)**.
2. **Discounting above 20% turns orders unprofitable** — margin drops from +29.5% at 0% discount, to +11.9% at 1-20%, to **-15.3% at 21-40%, and -77.4% at 41%+ discount**. This is a direct, actionable pricing-policy finding.
3. **West is the top-performing region** by sales ($725,355, 15% margin), while **Central has the thinnest regional margin** (7.9%) despite meaningful sales volume.
4. **Consumer is the leading customer segment** by both sales ($1.16M) and profit ($134K), ahead of Corporate and Home Office.
5. Peak sales month across the whole dataset was **November 2017** — consistent with holiday-season retail demand.
6. **Same Day shipping** has 0-day average delay vs. **5 days for Standard Class**, a useful benchmark for logistics SLA discussions.

## Visuals
See `superstore_dashboard.png` — a 6-panel dashboard covering:
- Sales by category
- Profit by sub-category (loss-making lines highlighted in red)
- Monthly sales trend (2014–2017)
- Profit margin % by discount band
- Sales by region
- Sales distribution by category (boxplot)

## Tech Stack
Python · Pandas · NumPy · Matplotlib · Seaborn

## How to Run
```bash
# 1. Install dependencies
pip install pandas numpy matplotlib seaborn

# 2. Place Sample_-_Superstore.csv in the same folder as the script

# 3. Run the analysis
python eda_superstore.py
```
This will print the full audit/cleaning/analysis log to the console, and produce:
- `superstore_clean.csv` — the cleaned dataset
- `eda_findings_superstore.txt` — full text output of the analysis
- `superstore_dashboard.png` — the 6-panel visual summary

## Files
- `eda_superstore.py` — full cleaning + analysis + visualization pipeline
- `Sample_-_Superstore.csv` — raw dataset
- `superstore_clean.csv` — cleaned dataset
- `eda_findings_superstore.txt` — full text output of the analysis
- `superstore_dashboard.png` — visual summary
