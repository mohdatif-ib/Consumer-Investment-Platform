# Implementation Guide

## 1. Environment Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Use Python 3.10 or later.

## 2. Run the ETL Pipeline

```powershell
$env:PYTHONPATH="src"
python -m consumer_brand_intel.etl_pipeline `
  --input data/raw/startup_funding_sample.csv `
  --output-dir data/processed
```

Optional PostgreSQL load:

```powershell
python -m consumer_brand_intel.etl_pipeline `
  --input data/raw/startup_funding_sample.csv `
  --output-dir data/processed `
  --database-url "postgresql://user:password@localhost:5432/consumer_brand_intel"
```

## 3. Create PostgreSQL Schema

```sql
\i sql/schema.sql
```

Load processed CSVs into the matching tables with your preferred PostgreSQL loader, or use the SQLAlchemy ETL load.

## 4. Generate Startup Rankings

```powershell
$env:PYTHONPATH="src"
python -m consumer_brand_intel.startup_scoring `
  --processed-dir data/processed `
  --output outputs/top_50_startups.csv
```

Methodology:

- Funding Growth measures latest annual funding growth per startup.
- Investor Quality scores investors by total invested, round activity, and startup breadth, then averages the quality of each startup's investor syndicate.
- Sector Growth measures latest annual funding growth for each sector.
- Funding Consistency rewards companies that raise capital steadily rather than erratically.

Assumptions:

- Multi-investor rounds are split equally across disclosed investors for investment bridge-table reporting.
- Unknown currencies default to a 1:1 USD conversion until an updated exchange-rate table is supplied.
- Funding momentum is treated as a proxy for market validation, not as proof of profitability.

## 5. Generate Forecasts

```powershell
$env:PYTHONPATH="src"
python -m consumer_brand_intel.forecasting `
  --processed-dir data/processed `
  --output-dir outputs `
  --periods 12
```

Forecasting includes:

- Linear Regression on monthly funding trend.
- ARIMA(1,1,1) when `statsmodels` is installed and enough observations exist.
- A moving-average fallback if ARIMA dependencies or sample length are insufficient.

## 6. Generate an Investment Memo

```powershell
$env:PYTHONPATH="src"
python -m consumer_brand_intel.investment_memo_generator `
  --company-name "GlowNest" `
  --processed-dir data/processed `
  --rankings-path outputs/top_50_startups.csv `
  --output outputs/glownest_investment_memo.md
```

## 7. Power BI Build

1. Connect Power BI to PostgreSQL or import the CSVs from `data/processed` and `outputs`.
2. Create relationships as documented in `powerbi/dashboard_spec.md`.
3. Add the DAX measures from the dashboard specification.
4. Build the six dashboard pages: Executive Overview, Sector Analysis, Investor Analysis, Geographic Analysis, Investment Opportunities, and Forecasting.
5. Export screenshots to `docs/screenshots/` for the README placeholders.

## 8. Portfolio Review Checklist

- ETL runs from raw CSV to normalized tables.
- SQL schema and advanced queries are present.
- Notebooks cover cleaning, EDA, scoring, and forecasting.
- Power BI specification includes data model, visuals, and DAX.
- README explains the business value, architecture, outputs, and future improvements.

