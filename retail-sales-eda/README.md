# Retail Sales EDA — Data Cleaning & Business Insights

An end-to-end exploratory data analysis project on a retail sales transactions dataset, covering data quality auditing, cleaning, and business-insight generation using Python (Pandas, NumPy, Matplotlib, Seaborn).

> **Note on the data:** this project uses a self-generated synthetic dataset (`generate_data.py`) modeled on realistic retail transaction patterns — categories, regional split, seasonality, discounts — with deliberately injected real-world messiness (missing values, duplicates, outliers, inconsistent text casing, mis-logged negative quantities). This was done so the cleaning and EDA logic reflects genuine data-quality problems, the same way a real internal sales dataset would.

## What this project demonstrates
- **Data quality auditing:** systematically identifying missing values, duplicate records, invalid values, and statistical outliers before any analysis.
- **Data cleaning:** text normalization, duplicate removal, outlier capping (IQR/winsorizing), and mode-based imputation for categorical fields.
- **Exploratory data analysis:** category/region/channel performance breakdowns, monthly trend analysis, and discount-vs-margin relationship analysis.
- **Insight generation:** translating raw statistics into concrete, decision-relevant business findings.

## Dataset
- 12,180 raw transaction records (12,001 after deduplication) across 2 years (2023–2024)
- Fields: Order ID, Date, Category, Product, Region, Channel, Payment Method, Quantity, Unit Price, Discount %, Gross Sales, Net Sales, Profit

## Data Quality Issues Found & Fixed
| Issue | Count | Fix Applied |
|---|---|---|
| Missing `Region` | 421 | Imputed with mode (most frequent region) |
| Missing `PaymentMethod` | 240 | Imputed with mode |
| Duplicate transaction rows | 179 | Removed |
| Negative `Quantity` (mis-logged returns) | 8 | Converted to absolute value |
| `NetSales` statistical outliers (IQR method) | 1,482 | Capped at IQR upper bound |
| Inconsistent `Category` text casing/whitespace | ~720 | Normalized via `.str.strip().str.title()` |

## Key Findings
1. **Electronics is the dominant revenue driver**, contributing ~72% of total net sales — far ahead of the next category.
2. **Revenue concentration risk:** the top 2 categories (Electronics, Home & Kitchen) together account for ~89% of total revenue, indicating heavy reliance on a narrow product mix.
3. **Discounting above 20% materially erodes margin** — profit margin drops from 44.7% (no discount) to 10.3% (21%+ discount band), suggesting the discount policy needs a cap or tiered approval process.
4. **Clear Q4 seasonality**, with peak sales in October, aligned with holiday-season demand in Electronics and Apparel.
5. **Online is the leading sales channel** by both order volume and revenue, ahead of In-Store and Marketplace.

## Visuals
See `eda_dashboard.png` — a 4-panel dashboard covering:
- Net sales by category
- Monthly sales trend
- Profit margin % by discount band
- Net sales distribution by category (boxplot, post-cleaning)

## Tech Stack
Python · Pandas · NumPy · Matplotlib · Seaborn

## How to run
```bash
pip install pandas numpy matplotlib seaborn
python generate_data.py     # creates retail_sales_raw.csv
python eda_analysis.py      # cleans data, runs EDA, saves findings + dashboard
```

## Files
- `generate_data.py` — synthetic dataset generator
- `eda_analysis.py` — cleaning + analysis + visualization pipeline
- `retail_sales_raw.csv` — raw (messy) dataset
- `retail_sales_clean.csv` — cleaned dataset
- `eda_findings.txt` — full text output of the analysis
- `eda_dashboard.png` — visual summary
