# Data Dictionary

## Raw Dataset: `data/raw/startup_funding_sample.csv`

| Column | Description |
|---|---|
| `company_name` | Startup or consumer brand name. |
| `sector` | Consumer category such as Food & Beverage, Beauty & Personal Care, or Health & Wellness. |
| `city` | Company headquarters city. |
| `founded_year` | Year the company was founded. |
| `funding_date` | Date of disclosed funding round. |
| `funding_stage` | Funding round stage such as Seed, Series A, Series B, Series C, or Growth. |
| `amount` | Funding amount in original currency. |
| `currency` | Original funding currency. |
| `investors` | Semicolon-delimited investor syndicate. |
| `startup_description` | Short business description used by the memo generator. |

## Processed Tables

| Table | Grain |
|---|---|
| `startups` | One row per startup. |
| `funding_rounds` | One row per disclosed funding round. |
| `investors` | One row per investor. |
| `investments` | One row per investor participation in a funding round. |
| `funding_events` | Clean denormalized event table for notebooks and BI. |
| `metrics` | Portfolio-level KPI snapshot. |

