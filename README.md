# Consumer Brand Investment Intelligence Platform

## Executive Summary

The Consumer Brand Investment Intelligence Platform is an end-to-end analytics project that helps venture capital, private equity, consulting, and corporate strategy teams evaluate emerging consumer brands using funding, investor, sector, geography, and growth signals.

### What problem does this project solve?

Consumer investors often screen hundreds of startups across fragmented datasets. Funding announcements, investor participation, sector momentum, and company growth indicators are usually reviewed manually in spreadsheets or disconnected tools. This project turns that process into a repeatable analytics workflow: clean the data, model it, analyze trends, rank startups, forecast funding activity, and generate an investment memo.

### Who is the target user?

| User | Need |
|---|---|
| Venture capital analysts | Prioritize startups for deeper diligence. |
| Private equity associates | Identify attractive consumer categories and acquisition themes. |
| Corporate development teams | Track emerging brands and potential partnership targets. |
| Consulting teams | Support market scans, investment theses, and client strategy work. |
| Data analytics recruiters | Evaluate data engineering, analytics, SQL, BI, and modeling ability in one project. |

### Why does this project matter?

Investment teams do not only need dashboards. They need decision systems that connect market data to action. This platform demonstrates how a raw funding dataset can become a structured decision-support product with analytical tables, SQL queries, Python models, forecast outputs, Power BI specifications, and an investment memo workflow.

## Business Problem

### Industry context

Consumer brands operate in categories where taste, timing, distribution, customer acquisition costs, and channel strategy can change quickly. Investors evaluating food, beauty, wellness, pet care, retail technology, apparel, and home brands need to answer two questions at the same time:

1. Is the category attractive?
2. Is this specific company showing enough momentum to deserve diligence?

Traditional startup screening relies on analyst research, CRM notes, funding databases, pitch decks, and manual Excel work. Those inputs are useful, but they can be slow and inconsistent when analysts need to compare many companies across sectors and geographies.

### Pain points

| Pain Point | Impact |
|---|---|
| Funding data is messy and duplicated | Analysts spend time cleaning instead of interpreting. |
| Investor names and rounds are stored as text | It is hard to analyze syndicates and investor activity. |
| Sector and geography cuts are manual | Pattern recognition depends on analyst bandwidth. |
| Startup prioritization is subjective | Teams may miss companies with strong growth signals. |
| Forecasting is disconnected from dashboards | Market outlook is not always tied to current pipeline views. |
| Memo writing is repetitive | Analysts recreate similar thesis, risk, and opportunity language for each startup. |

### Existing alternatives

| Alternative | Strength | Limitation |
|---|---|---|
| Crunchbase, PitchBook, Tracxn, Dealroom | Broad market coverage | Expensive, not always customized to internal investment logic. |
| Excel and Google Sheets | Flexible and familiar | Error-prone at scale, weak reproducibility, limited modeling structure. |
| BI dashboards alone | Good for visual exploration | Do not automatically rank opportunities or generate investment narratives. |
| CRM exports | Useful internal pipeline context | Often incomplete for sector-level and investor-level market analysis. |

### Why this solution is valuable

This project combines data engineering, analytics, scoring, forecasting, and BI design into one workflow. The value is not only in the individual reports; it is in the repeatable decision process. A firm can refresh the raw CSVs, regenerate clean tables, rerun scoring, update forecasts, and feed the results into Power BI.

Assumption: this repository uses a synthetic sample dataset for portfolio demonstration. In production, the same workflow could be connected to Crunchbase, PitchBook, Dealroom, Tracxn, proprietary CRM exports, web traffic data, retail sell-through data, or internal diligence files.

## Project Objectives

| Objective | Measurable Goal |
|---|---|
| Reduce manual analysis time | Convert raw funding CSVs into clean analytical tables through an automated ETL pipeline. |
| Improve decision-making | Rank startups with a transparent, weighted investment attractiveness model. |
| Automate repetitive tasks | Generate processed tables, top-startup rankings, forecasts, and investment memos from command-line scripts. |
| Generate actionable insights | Identify top sectors, top cities, active investors, fastest-growing categories, and priority companies. |
| Build a BI-ready data model | Provide PostgreSQL schema, Power BI relationships, and DAX measures. |
| Demonstrate production thinking | Use modular code, validation, error handling, tests, documentation, and reproducible outputs. |

## Architecture Overview

### System design

The platform is designed as a layered analytics system:

1. Raw data layer: startup funding CSV files.
2. ETL layer: Python cleaning and normalization.
3. Analytical data layer: normalized startup, funding, investor, and investment tables.
4. SQL layer: PostgreSQL schema and reusable business queries.
5. Analytics layer: notebooks for exploration and interpretation.
6. Modeling layer: scoring and forecasting scripts.
7. BI layer: Power BI dashboard specification and DAX measures.
8. Decision-support layer: AI-style investment memo generator.

### Data flow

```mermaid
flowchart LR
    A["Raw funding CSV files"] --> B["ETL pipeline"]
    B --> C["Clean funding events"]
    C --> D["Normalized tables"]
    D --> E["PostgreSQL schema"]
    D --> F["Exploratory notebooks"]
    D --> G["Startup scoring engine"]
    D --> H["Forecasting models"]
    G --> I["Top 50 startup rankings"]
    H --> J["12-month funding forecasts"]
    H --> K["Fastest-growing sectors"]
    E --> L["Power BI dashboard"]
    I --> L
    J --> L
    I --> M["Investment memo generator"]
    C --> M
```

### Components

| Component | Description |
|---|---|
| ETL pipeline | Loads raw CSVs, standardizes fields, converts currencies, removes duplicates, and writes clean tables. |
| PostgreSQL schema | Stores startups, funding rounds, investors, and investments with primary keys and foreign keys. |
| Analytics notebooks | Provide sector, investor, geographic, funding trend, scoring, and forecasting analysis. |
| Scoring engine | Ranks startups using funding growth, investor quality, sector growth, and funding consistency. |
| Forecasting module | Predicts next 12 months of funding activity with Linear Regression and ARIMA. |
| Power BI spec | Defines dashboard pages, visuals, relationships, and DAX measures. |
| Memo generator | Produces a structured VC-style memo with thesis, risks, opportunities, and recommendation score. |

### Folder structure

```text
consumer-brand-investment-intelligence-platform/
  data/
    raw/
      startup_funding_sample.csv
    processed/
      startups.csv
      funding_rounds.csv
      investors.csv
      investments.csv
      funding_events.csv
      metrics.csv
  docs/
    data_dictionary.md
    implementation_guide.md
  notebooks/
    01_data_cleaning.ipynb
    02_exploratory_analysis.ipynb
    03_startup_scoring.ipynb
    04_forecasting.ipynb
  outputs/
    top_50_startups.csv
    funding_forecasts.csv
    fastest_growing_sectors.csv
    glownest_investment_memo.md
  powerbi/
    dashboard_spec.md
  sql/
    schema.sql
    advanced_queries.sql
  src/
    consumer_brand_intel/
      data_cleaning.py
      etl_pipeline.py
      startup_scoring.py
      forecasting.py
      investment_memo_generator.py
  tests/
    test_pipeline.py
  pyproject.toml
  requirements.txt
  README.md
```

## Tech Stack

| Technology | Purpose | Why it was chosen |
|---|---|---|
| Python | Core ETL, analytics, scoring, forecasting, and memo generation | Python is widely used in data engineering and analytics, with strong libraries for tabular processing and modeling. |
| Pandas | Data loading, cleaning, grouping, reshaping, and CSV outputs | Best fit for structured funding data and rapid analytical transformations. |
| NumPy | Numerical operations, arrays, ranking helpers, fallback regression | Provides efficient mathematical operations and supports model calculations. |
| Scikit-Learn | MinMax normalization and Linear Regression | Standard machine learning library with readable APIs and recruiter-recognized usage. |
| Statsmodels | ARIMA time-series forecasting | Provides classical statistical forecasting suitable for funding trend analysis. |
| PostgreSQL | Relational database schema and SQL analytics | Strong fit for normalized investor, startup, funding round, and investment tables. |
| SQLAlchemy | Optional Python-to-PostgreSQL loading | Allows the ETL pipeline to write tables directly to a database when credentials are provided. |
| Matplotlib | Notebook visualization support | Common baseline plotting library for analytical workflows. |
| Plotly | Interactive charts in notebooks and dashboard-like exploration | Useful for recruiter demos and exploratory analysis. |
| Power BI | Executive dashboard layer | Common enterprise BI tool used by finance, consulting, and analytics teams. |
| DAX | Power BI business measures | Enables reusable KPIs such as Total Funding, Average Deal Size, and YoY Growth. |
| Pytest | Pipeline and scoring tests | Validates important contracts: raw data in, clean tables and rankings out. |

## Dataset / Data Sources

### Dataset 1: Startup funding sample

| Attribute | Details |
|---|---|
| Source | Synthetic portfolio dataset created for this project. |
| File | `data/raw/startup_funding_sample.csv` |
| Description | Funding events for consumer brands across food, beauty, wellness, pet care, retail tech, apparel, and home categories. |
| Number of records | 39 raw funding events. |
| Key fields | `company_name`, `sector`, `city`, `founded_year`, `funding_date`, `funding_stage`, `amount`, `currency`, `investors`, `startup_description`. |
| Limitations | Synthetic data, limited sample size, no revenue, margin, customer retention, valuation, web traffic, or real-time FX feed. |

### Processed analytical tables

| Table | Records | Grain | Purpose |
|---|---:|---|---|
| `startups.csv` | 15 | One row per startup | Company dimension for sector, city, founded year, and description. |
| `funding_rounds.csv` | 39 | One row per funding round | Round-level amount, stage, date, and startup relationship. |
| `investors.csv` | 10 | One row per investor | Investor dimension for syndicate analysis. |
| `investments.csv` | 78 | One row per investor participation | Bridge table between startups, investors, and rounds. |
| `funding_events.csv` | 39 | One row per cleaned funding event | Denormalized table for notebooks, scoring, and memo generation. |
| `metrics.csv` | 1 | Portfolio KPI snapshot | Total funding, average deal size, growth, investor count, and round count. |

### Current sample KPI snapshot

| Metric | Value |
|---|---:|
| Total funding | $416,643,000 |
| Average deal size | $10,683,153.85 |
| Latest-year funding growth | 105.86% |
| Number of investors | 10 |
| Number of funding rounds | 39 |

## Business Questions Answered

This platform is designed to answer the questions investment teams ask during market mapping and early diligence:

1. Which consumer sectors receive the most funding?
2. Which sectors are growing fastest year over year?
3. Which cities have the highest concentration of funded consumer brands?
4. Which startups have raised the most capital?
5. Which startups show the strongest funding growth?
6. Which startups have the most attractive combination of growth, investor quality, sector growth, and consistency?
7. Which investors participate in the most rounds?
8. Which investors have the broadest consumer startup portfolios?
9. Which investors are concentrated in specific sectors?
10. What is the average deal size by funding stage?
11. How has total funding changed by year?
12. Which funding stages dominate the sample market?
13. Which startups have progressed from Seed to later-stage rounds?
14. Which cities are emerging as consumer startup hubs?
15. Which sectors are most suitable for proactive thesis development?
16. What funding activity is forecasted over the next 12 months?
17. Which startups should be prioritized for partner review?
18. What risks and opportunities should be summarized in an investment memo?

## Solution Approach

### 1. Data Collection

The project starts with a structured CSV containing funding events. The pipeline supports one or more CSV files, so additional datasets can be appended without changing the downstream logic as long as the required columns are present.

### 2. Data Cleaning

The cleaning module:

- Normalizes column names.
- Validates required fields.
- Standardizes text fields such as sector, city, funding stage, currency, and investors.
- Parses monetary values.
- Converts funding dates to datetime.
- Converts original currencies into USD using a configurable exchange-rate dictionary.
- Removes duplicate funding events using company, date, stage, and USD amount.
- Assigns stable event IDs.

### 3. Data Modeling

The project converts cleaned events into normalized analytical tables:

- `startups`: company dimension.
- `funding_rounds`: round fact table.
- `investors`: investor dimension.
- `investments`: bridge table for many-to-many investor participation.
- `funding_events`: denormalized table for analytics and modeling.
- `metrics`: KPI snapshot.

This design supports both SQL analysis and Power BI modeling.

### 4. Analytics

The analytics workflow calculates:

- Total funding.
- Average deal size.
- Number of startups.
- Number of investors.
- Number of funding rounds.
- Funding by sector.
- Funding by city.
- Funding over time.
- Investor activity.
- Funding stage distribution.

### 5. Scoring Logic

The startup scoring engine creates a transparent investment attractiveness score:

| Component | Weight | Interpretation |
|---|---:|---|
| Funding Growth | 40% | Measures whether a startup is raising larger rounds over time. |
| Investor Quality | 30% | Estimates strength of the investor syndicate using investor activity and capital participation. |
| Sector Growth | 20% | Rewards startups operating in categories with funding momentum. |
| Funding Consistency | 10% | Rewards startups with repeatable funding patterns instead of erratic round sizes. |

Each component is normalized before weighting so features with different units can be compared fairly.

### 6. Forecasting

The forecasting module aggregates funding by month and predicts the next 12 months using:

- Linear Regression for a simple directional trend baseline.
- ARIMA(1,1,1) for time-series forecasting when enough observations and dependencies are available.
- Moving-average fallback if ARIMA cannot be used.

### 7. Dashboard Creation

The Power BI specification translates the analytical model into six pages:

1. Executive Overview
2. Sector Analysis
3. Investor Analysis
4. Geographic Analysis
5. Investment Opportunities
6. Forecasting

The dashboard spec includes data model relationships, expected visuals, design notes, and DAX measures.

## Code Walkthrough

### `src/consumer_brand_intel/data_cleaning.py`

**Purpose**

Turns raw startup funding CSV data into clean, normalized analytical tables.

**Inputs**

- One or more raw CSV files with startup funding event data.
- Optional exchange-rate dictionary for currency standardization.

**Outputs**

- `startups.csv`
- `funding_rounds.csv`
- `investors.csv`
- `investments.csv`
- `funding_events.csv`
- `metrics.csv`

**Key functions and classes**

| Function or Class | Explanation |
|---|---|
| `CleanedTables` | Dataclass that packages all processed tables into one object. |
| `load_csv_files()` | Reads one or more raw CSV files and combines them into one DataFrame. |
| `validate_schema()` | Checks that required business fields are present before transformation. |
| `parse_money()` | Converts numeric or formatted funding amounts into floats. |
| `clean_raw_funding_data()` | Performs the main cleaning logic: text cleanup, date parsing, missing values, currency conversion, and deduplication. |
| `build_analytical_tables()` | Converts cleaned events into normalized startup, round, investor, and investment tables. |
| `calculate_platform_metrics()` | Produces the top-level KPI snapshot. |
| `save_cleaned_tables()` | Writes processed tables to CSV. |
| `clean_csv_files()` | End-to-end helper for loading, cleaning, modeling, and saving. |

**Simplified explanation**

The module takes messy funding data and answers: "What are the clean business entities?" A company becomes a startup record, each funding event becomes a funding round, each investor becomes an investor record, and each investor's participation becomes an investment record.

### `src/consumer_brand_intel/etl_pipeline.py`

**Purpose**

Provides a command-line pipeline for running the data cleaning workflow and optionally loading tables into PostgreSQL.

**Inputs**

- Raw CSV file paths.
- Output directory.
- Optional PostgreSQL connection URL.

**Outputs**

- Processed CSV files.
- Optional PostgreSQL tables.

**Key functions**

| Function | Explanation |
|---|---|
| `configure_logging()` | Sets up readable ETL logging. |
| `load_tables_to_postgres()` | Loads processed tables into PostgreSQL using SQLAlchemy. |
| `run_etl()` | Orchestrates the full ETL workflow. |
| `parse_args()` | Defines command-line inputs. |
| `main()` | Entry point for command-line execution. |

**Simplified explanation**

This is the operational wrapper. Instead of opening notebooks manually, a user can run one command to process raw files and produce the analytical layer.

### `src/consumer_brand_intel/startup_scoring.py`

**Purpose**

Ranks startups by investment attractiveness using a transparent VC-style scoring framework.

**Inputs**

- `funding_events.csv`
- `investments.csv`
- `investors.csv`

**Outputs**

- `outputs/top_50_startups.csv`

**Key functions**

| Function | Explanation |
|---|---|
| `_safe_growth()` | Calculates growth while avoiding divide-by-zero errors. |
| `_normalize()` | Scales features between 0 and 1 using Scikit-Learn or a NumPy fallback. |
| `build_scoring_features()` | Engineers startup growth, sector growth, investor quality, total funding, average deal size, and consistency features. |
| `score_startups()` | Applies weights and creates the final investment attractiveness score. |
| `rank_startups()` | Loads processed files, ranks startups, and writes the top-ranked output. |

**Simplified explanation**

The scoring model is not a black box. It creates interpretable features, normalizes them, applies weights, and ranks companies. A recruiter or investor can inspect why a startup scored well.

### `src/consumer_brand_intel/forecasting.py`

**Purpose**

Forecasts future funding activity and identifies fastest-growing sectors.

**Inputs**

- `funding_events.csv`

**Outputs**

- `outputs/funding_forecasts.csv`
- `outputs/fastest_growing_sectors.csv`

**Key functions**

| Function | Explanation |
|---|---|
| `load_monthly_funding()` | Aggregates funding events into monthly totals. |
| `forecast_with_linear_regression()` | Builds a trend-based forecast for the next 12 months. |
| `forecast_with_arima()` | Uses ARIMA for time-series forecasting when available. |
| `identify_fastest_growing_sectors()` | Calculates latest year-over-year funding growth by sector. |
| `generate_forecasts()` | Runs both forecasting models and writes output files. |

**Simplified explanation**

This module turns historical monthly funding into a forward-looking market view. Linear Regression provides an easy-to-explain baseline; ARIMA provides a classical time-series alternative.

### `src/consumer_brand_intel/investment_memo_generator.py`

**Purpose**

Generates a structured VC-style investment memo for a selected startup.

**Inputs**

- Startup name.
- Processed funding events.
- Optional ranking score from the scoring model.

**Outputs**

- Markdown investment memo with thesis, risks, opportunities, score, and recommendation.

**Key functions and classes**

| Function or Class | Explanation |
|---|---|
| `InvestmentMemo` | Dataclass representing the memo output. |
| `generate_memo()` | Builds the investment thesis, opportunity bullets, risk bullets, and score. |
| `memo_from_processed_data()` | Loads processed data for one startup and generates the memo. |

**Simplified explanation**

The memo generator converts quantitative signals into written investment logic. It is intentionally deterministic so the project can run without API keys.

### Notebooks

| Notebook | Purpose |
|---|---|
| `01_data_cleaning.ipynb` | Demonstrates raw-to-clean table creation. |
| `02_exploratory_analysis.ipynb` | Explores sectors, cities, investors, funding trends, and stage distribution. |
| `03_startup_scoring.ipynb` | Shows feature engineering and ranking output. |
| `04_forecasting.ipynb` | Demonstrates monthly forecasting and fastest-growing sector analysis. |

## SQL Explanation

### Schema design

The PostgreSQL schema uses a normalized relational model:

```mermaid
erDiagram
    startups ||--o{ funding_rounds : has
    startups ||--o{ investments : receives
    investors ||--o{ investments : makes
    funding_rounds ||--o{ investments : contains

    startups {
        integer startup_id PK
        varchar company_name
        varchar sector
        varchar city
        integer founded_year
        text startup_description
    }

    funding_rounds {
        integer round_id PK
        integer startup_id FK
        date funding_date
        varchar funding_stage
        numeric amount
    }

    investors {
        integer investor_id PK
        varchar investor_name
    }

    investments {
        integer investment_id PK
        integer startup_id FK
        integer investor_id FK
        integer round_id FK
        numeric amount
    }
```

### Relationships

| Relationship | Reason |
|---|---|
| `startups` to `funding_rounds` | One startup can have many funding rounds. |
| `startups` to `investments` | One startup can receive many investor participations. |
| `investors` to `investments` | One investor can participate in many startup investments. |
| `funding_rounds` to `investments` | One round can include multiple investors. |

### Important queries

| Query | Business purpose | SQL technique |
|---|---|---|
| Top funded sectors | Identify category-level capital concentration. | Join startups to funding rounds, group by sector, sum amount. |
| Top funded cities | Identify geographic startup hubs. | Join startups to funding rounds, group by city. |
| Most active investors | Identify syndicate leaders and market makers. | Join investors to investments, count rounds and startups. |
| Average deal size by stage | Compare capital intensity across stages. | Group funding rounds by stage and calculate average and median. |
| Funding growth by year | Track market momentum. | Use CTE and `LAG()` window function for YoY growth. |
| Startup funding history | View company-level funding progression. | Use cumulative `SUM()` window function by startup. |
| Investor-sector concentration | Understand investor category focus. | Join investments, investors, and startups, then group by investor and sector. |

### Why joins and aggregations were used

The normalized schema avoids repeating investor and startup attributes in every row. Joins reconstruct business views only when needed. Aggregations then answer investment questions at the right level: sector, city, investor, stage, year, or startup.

## Analytics Explanation

### KPIs

| KPI | Calculation | Business meaning |
|---|---|---|
| Total Funding | Sum of USD funding amounts | Size of the observable funding market. |
| Average Deal Size | Total funding divided by funding rounds | Typical check or round size. |
| Funding Growth | Year-over-year funding change | Market momentum. |
| Number of Investors | Distinct investor names | Breadth of capital providers. |
| Number of Funding Rounds | Distinct funding events | Deal activity. |
| Investor Participation | Distinct rounds per investor | Investor activity level. |
| Startup Ranking Score | Weighted normalized model score | Prioritization signal for diligence. |
| Forecasted Funding | Sum of predicted monthly funding | Forward-looking market view. |

### Assumptions

| Assumption | Rationale |
|---|---|
| Multi-investor rounds are split equally in the `investments` table | The raw sample does not provide individual investor check sizes. |
| Static exchange rates are acceptable for demo data | Production would use a dated FX table or API. |
| Funding growth is a proxy for market validation | It indicates investor demand, but not profitability or unit economics. |
| Investor quality can be estimated from activity and capital breadth | Stronger investors often participate in more rounds and support more companies. |
| Forecasting is directional, not deterministic | A 39-record synthetic dataset is not enough for institutional forecast confidence. |

## Models and Algorithms

### Startup scoring model

| Aspect | Explanation |
|---|---|
| Why selected | Investment screening requires an interpretable ranking system, not a black-box model. |
| How it works | Features are engineered, normalized to 0-1, weighted, summed, multiplied by 100, and ranked. |
| Features | Funding growth, investor quality, sector growth, funding consistency. |
| Limitations | Does not include revenue, valuation, margins, retention, customer acquisition costs, or founder quality. |
| Improvements | Add valuation-adjusted growth, customer cohort data, retail velocity, revenue CAGR, gross margin, and qualitative diligence scoring. |

### Linear Regression forecasting

| Aspect | Explanation |
|---|---|
| Why selected | Provides a simple trend baseline that is easy to explain to nontechnical stakeholders. |
| How it works | Fits a line to monthly funding totals and extrapolates future months. |
| Limitations | Assumes a linear trend and does not handle seasonality or sudden funding shocks well. |
| Improvements | Add sector-specific models, cross-validation, confidence intervals, and macroeconomic features. |

### ARIMA forecasting

| Aspect | Explanation |
|---|---|
| Why selected | ARIMA is a classical time-series method for modeling trend and autocorrelation. |
| How it works | Uses differencing and autoregressive/moving-average terms to forecast future monthly funding. |
| Limitations | Needs more observations than this synthetic sample provides for reliable production forecasts. |
| Improvements | Tune `(p,d,q)` with AIC/BIC, evaluate out-of-sample error, add SARIMA for seasonality, and forecast by sector. |

### Investment memo generator

| Aspect | Explanation |
|---|---|
| Why selected | Analysts often need quick first-pass memos during screening. |
| How it works | Combines startup description, funding history, sector, growth, and ranking score into structured memo sections. |
| Limitations | Deterministic text templates cannot replace full diligence or LLM-based reasoning over richer documents. |
| Improvements | Connect to an LLM, add source citations, include founder background, revenue metrics, competitor mapping, and diligence checklists. |

## Results and Insights

### Key findings from the sample run

| Finding | Evidence | Business implication |
|---|---|---|
| Food & Beverage is the largest funded sector | $121.21M total funding | The category may be the largest capital pool in this sample. |
| Beauty & Personal Care ranks second by capital raised | $103.22M total funding | Beauty remains a strong consumer investment theme. |
| Health & Wellness is also material | $82.30M total funding | Wellness brands show continued investor appetite. |
| Pet Care is the fastest-growing sector | 162.35% latest-year growth | Smaller category but strong momentum signal. |
| GlowNest ranks first in attractiveness score | 74.81 score | High-growth beauty startup with strong investor participation. |
| SkinTheory has the highest total funding among ranked startups | $61.10M | Later-stage beauty company may be a mature diligence target. |
| Chicago is the top funded city in the sample | $73.00M total funding | FreshForge drives strong city-level funding concentration. |
| Linear Regression forecasts $325.43M over the next 12 months | Sum of forecasted monthly funding | Trend baseline suggests continued funding expansion. |
| ARIMA forecasts $298.02M over the next 12 months | Sum of ARIMA forecasted monthly funding | Alternative time-series view is slightly more conservative. |

### Top 10 ranked startups

| Rank | Startup | Sector | City | Score |
|---:|---|---|---|---:|
| 1 | GlowNest | Beauty & Personal Care | Los Angeles | 74.81 |
| 2 | SkinTheory | Beauty & Personal Care | Miami | 66.85 |
| 3 | KindCart | Retail Tech | Boston | 64.56 |
| 4 | AuraSnack | Food & Beverage | Austin | 62.54 |
| 5 | LoopWear | Fashion & Apparel | New York | 62.24 |
| 6 | FreshForge | Food & Beverage | Chicago | 61.04 |
| 7 | PetPulse | Pet Care | Denver | 59.32 |
| 8 | VitaBloom | Health & Wellness | San Francisco | 58.02 |
| 9 | BrightBrew | Food & Beverage | Portland | 53.82 |
| 10 | HomeMint | Home & Lifestyle | Seattle | 49.77 |

### Business implications

The results show how the platform can separate market size from momentum. Food & Beverage has the most total capital, but Pet Care has the strongest latest-year growth. Beauty & Personal Care has both high total funding and two of the top-ranked startups, which makes it a strong category for deeper thesis work.

## Questions Recruiters May Ask

### 1. Why did you normalize the scoring variables?

**Concise answer:** The model combines features with different units, so normalization makes them comparable.

**Technical explanation:** Funding growth, investor quality, sector growth, and consistency have different scales. MinMax normalization converts them to a 0-1 range before weighting.

**Business explanation:** Without normalization, one large-number feature could dominate the ranking and create misleading investment recommendations.

### 2. Why use a transparent weighted score instead of a complex ML model?

**Concise answer:** Investment screening needs explainability.

**Technical explanation:** The score is calculated from explicit components and weights, so each ranking can be traced back to interpretable drivers.

**Business explanation:** Partners and investment committees need to understand why a startup is recommended before acting on it.

### 3. How did you define investor quality?

**Concise answer:** Investor quality is estimated from total invested amount, number of rounds, and number of startups backed.

**Technical explanation:** The model calculates investor-level activity metrics and averages those scores across each startup's investor syndicate.

**Business explanation:** Active investors with broader portfolios may indicate stronger market validation and better follow-on support.

### 4. What is the biggest limitation of the dataset?

**Concise answer:** It is synthetic and does not include revenue, valuation, or customer metrics.

**Technical explanation:** The dataset has 39 funding events, which is enough to demonstrate workflow design but not enough for institutional model confidence.

**Business explanation:** Funding data is useful for screening, but real diligence needs unit economics, retention, margin, channel mix, and founder assessment.

### 5. Why did you split multi-investor rounds equally?

**Concise answer:** The raw data does not include individual investor check sizes.

**Technical explanation:** The ETL creates an `investments` bridge table by dividing the round amount across disclosed investors.

**Business explanation:** This preserves investor participation analysis while clearly documenting the allocation assumption.

### 6. Why design a normalized SQL schema?

**Concise answer:** Normalization reduces duplication and supports flexible analysis.

**Technical explanation:** Startups, investors, funding rounds, and investments are separated into related tables with keys.

**Business explanation:** Analysts can answer sector, city, investor, and startup questions without maintaining inconsistent repeated data.

### 7. What SQL concepts does this project demonstrate?

**Concise answer:** Joins, aggregations, indexes, constraints, CTEs, and window functions.

**Technical explanation:** The queries use foreign-key joins, grouped sums and averages, `LAG()` for YoY growth, and cumulative `SUM()` windows.

**Business explanation:** These techniques convert raw deal records into investor-ready insights.

### 8. Why include both notebooks and production scripts?

**Concise answer:** Notebooks explain analysis; scripts make the workflow repeatable.

**Technical explanation:** Business logic lives in modules under `src`, while notebooks call that logic for exploration.

**Business explanation:** This mirrors real analytics work where exploration and production workflows both matter.

### 9. How would you scale this project?

**Concise answer:** Move from CSV inputs to scheduled ingestion, database storage, orchestration, and monitoring.

**Technical explanation:** Add Airflow or Dagster, database migrations, incremental loads, logging, data quality checks, and cloud storage.

**Business explanation:** Scaling would allow an investment team to refresh market intelligence automatically.

### 10. Why use PostgreSQL?

**Concise answer:** It is reliable, widely used, and strong for relational analytics.

**Technical explanation:** PostgreSQL supports constraints, indexes, CTEs, window functions, and BI connectivity.

**Business explanation:** It gives analysts and dashboard tools a trusted central data model.

### 11. Why use Power BI?

**Concise answer:** Power BI is common in enterprise reporting and finance analytics.

**Technical explanation:** The project provides DAX measures, relationships, and dashboard page specifications.

**Business explanation:** It makes the insights accessible to nontechnical decision-makers.

### 12. What does the forecasting model predict?

**Concise answer:** It predicts monthly funding activity for the next 12 months.

**Technical explanation:** Funding events are resampled monthly, then forecasted with Linear Regression and ARIMA.

**Business explanation:** Investors can use forecasts to understand whether market activity is expanding or slowing.

### 13. Why include ARIMA?

**Concise answer:** ARIMA is a standard time-series benchmark.

**Technical explanation:** ARIMA models autoregressive and moving-average patterns after differencing.

**Business explanation:** It provides a more time-series-aware comparison to a simple linear trend.

### 14. What would improve the forecasts?

**Concise answer:** More historical data and external features.

**Technical explanation:** Add sector-level data, macro variables, interest rates, public market multiples, seasonality, and validation splits.

**Business explanation:** Better forecasts would help firms plan sourcing priorities and sector coverage.

### 15. What makes this project portfolio-grade?

**Concise answer:** It connects business context, engineering, SQL, analytics, modeling, BI, and documentation.

**Technical explanation:** The repository includes modular code, schema design, notebooks, outputs, tests, and setup instructions.

**Business explanation:** It resembles a real analytics product rather than a single isolated notebook.

### 16. How does the memo generator add value?

**Concise answer:** It turns data signals into an analyst-friendly narrative.

**Technical explanation:** It reads funding history, sector, startup description, and ranking score to produce a markdown memo.

**Business explanation:** It reduces repetitive first-pass memo writing and helps standardize screening notes.

### 17. How did you handle missing values?

**Concise answer:** Required fields are validated, text fields are filled with sensible defaults, and numeric fields are imputed when needed.

**Technical explanation:** The cleaning pipeline fills missing sectors and cities as `Unknown`, missing investors as `Undisclosed`, and missing amounts with the median.

**Business explanation:** This avoids breaking the pipeline while preserving data quality limitations for review.

### 18. How are duplicates removed?

**Concise answer:** Duplicate funding events are detected by company, funding date, stage, and USD amount.

**Technical explanation:** The pipeline applies `drop_duplicates()` on those fields after standardizing date and amount.

**Business explanation:** Duplicate funding announcements can inflate total funding and distort investment conclusions.

### 19. What would you change for production?

**Concise answer:** Add orchestration, monitoring, real data feeds, data contracts, and stronger validation.

**Technical explanation:** I would add scheduled jobs, Great Expectations or dbt tests, migrations, CI, and environment-specific configs.

**Business explanation:** Production users need trust, refresh reliability, and clear ownership of data quality.

### 20. How would you evaluate whether the ranking model works?

**Concise answer:** Compare scores against real investment outcomes.

**Technical explanation:** Backtest rankings against follow-on rounds, exits, revenue growth, valuation step-ups, or markups.

**Business explanation:** A good screening model should improve sourcing efficiency and identify companies that later prove attractive.

## Challenges Encountered

### Technical challenges

| Challenge | Resolution |
|---|---|
| Optional dependencies can block lightweight execution | The ETL imports SQLAlchemy only when PostgreSQL loading is requested. Scoring and forecasting include fallbacks when Scikit-Learn or Statsmodels are unavailable. |
| Investor syndicates are stored as semicolon-delimited text | The ETL splits investor strings and creates a normalized investor dimension plus investment bridge table. |
| Different currencies appear in the raw dataset | The cleaning pipeline maps currencies to configurable USD exchange rates. |
| Time-series sample size is small | Forecasting includes a simple trend model and documents ARIMA limitations. |
| Scoring features have different units | Features are normalized before applying model weights. |

### Data quality issues

| Issue | Handling |
|---|---|
| Missing optional descriptions | The cleaner creates an empty `startup_description` field if absent. |
| Missing founded years | Missing values are imputed with the median founded year. |
| Missing investors | Filled as `Undisclosed`. |
| Duplicate events | Removed using company, date, stage, and amount. |
| Unknown currencies | Default to 1.0 exchange rate unless a mapping is provided. |

### Scalability concerns

| Concern | Production approach |
|---|---|
| CSV files may become too large | Use cloud object storage and incremental database loads. |
| Static exchange rates may become inaccurate | Use dated FX reference tables or an FX API. |
| Manual dashboard refresh | Schedule Power BI refresh against PostgreSQL. |
| Model drift | Track score distributions and compare against investment outcomes. |
| Data lineage | Add orchestration metadata and run IDs. |

## Future Improvements

### Short-term improvements

- Add richer test coverage for currency parsing, investor splitting, and ranking edge cases.
- Add static type checking with `mypy`.
- Add data validation checks with Great Expectations or Pandera.
- Add a sample Power BI `.pbix` file once dashboard screenshots are created.
- Add command-line options for custom scoring weights.

### Long-term roadmap

- Connect to real funding data providers such as Crunchbase, PitchBook, Dealroom, Tracxn, or internal CRM exports.
- Add startup revenue, valuation, ARR, gross margin, retention, customer acquisition cost, and retail velocity.
- Build a dbt project for SQL transformations and documentation.
- Deploy the pipeline on Airflow, Dagster, or Prefect.
- Store data in PostgreSQL, Snowflake, BigQuery, or Redshift for enterprise-scale use.
- Add model backtesting against follow-on funding, exits, and valuation step-ups.

### AI enhancements

- Replace deterministic memo templates with an LLM-powered memo generator.
- Add retrieval-augmented generation over pitch decks, news, financial data, and customer reviews.
- Generate investor-specific outreach briefs based on investor sector preferences.
- Add risk extraction from filings, news, reviews, and market data.
- Create an analyst copilot that can answer questions over the SQL database.

### Production deployment ideas

- Scheduled ingestion pipeline with alerting.
- PostgreSQL database with migrations and role-based access.
- Power BI service deployment with refresh schedules.
- CI pipeline for tests and code quality checks.
- Dockerized application environment.
- Model monitoring dashboard for ranking drift and forecast error.

## What I Learned

Building this project reinforced that investment analytics is not just about producing charts. The hard part is designing a workflow that turns messy market data into decisions that a business user can trust.

### Technical skills learned

- Designing an ETL pipeline with validation, cleaning, deduplication, and repeatable outputs.
- Creating a normalized SQL schema with fact and dimension tables.
- Writing analytical SQL with joins, grouped aggregations, CTEs, and window functions.
- Building interpretable scoring logic with normalized features.
- Implementing forecasting with both a simple baseline and a classical time-series model.
- Structuring Python code as reusable modules instead of one-off notebook cells.
- Designing BI measures and dashboard pages from business requirements.

### Business skills learned

- Translating investor screening workflows into analytical requirements.
- Distinguishing market size from growth momentum.
- Thinking about the difference between a useful screening signal and a diligence conclusion.
- Communicating assumptions clearly so stakeholders understand model limits.
- Designing outputs for multiple audiences: analysts, partners, recruiters, and technical reviewers.

### Key takeaway

The most valuable analytics systems are not the most complicated ones. They are the ones that make assumptions visible, reduce manual work, and help decision-makers ask better follow-up questions.

## Resume Impact

- Built an end-to-end consumer investment analytics platform processing 39 funding events into 6 analytical tables, 15 ranked startups, 24 forecast rows, and a VC-style memo output.
- Designed a PostgreSQL schema with normalized startup, funding round, investor, and investment tables plus advanced SQL queries for sector, city, investor, growth, and funding history analysis.
- Developed a transparent startup scoring engine using weighted normalized features for funding growth, investor quality, sector growth, and funding consistency to prioritize investment opportunities.
- Created a Power BI-ready analytics layer with dashboard specifications, DAX measures, forecast outputs, and documented business logic for executive investment decision-making.

## Screenshots

Add screenshots after building the Power BI report and exporting visuals.

### Dashboard screenshots

| Page | Placeholder |
|---|---|
| Executive Overview | `docs/screenshots/executive_overview.png` |
| Sector Analysis | `docs/screenshots/sector_analysis.png` |
| Investor Analysis | `docs/screenshots/investor_analysis.png` |
| Geographic Analysis | `docs/screenshots/geographic_analysis.png` |
| Investment Opportunities | `docs/screenshots/investment_opportunities.png` |
| Forecasting | `docs/screenshots/forecasting.png` |

### Database schema

Placeholder:

```text
docs/screenshots/database_schema.png
```

### Architecture diagram

Placeholder:

```text
docs/screenshots/architecture_diagram.png
```

### Analytics visualizations

Placeholders:

```text
docs/screenshots/funding_by_sector.png
docs/screenshots/funding_by_city.png
docs/screenshots/funding_over_time.png
docs/screenshots/investor_activity.png
docs/screenshots/funding_stage_distribution.png
```

## Installation

### Prerequisites

- Python 3.10 or later.
- PostgreSQL, optional for database loading.
- Power BI Desktop, optional for dashboard build.

### Setup

```powershell
cd "D:\OneDrive\Documents\Data Analysis Project\consumer-brand-investment-intelligence-platform"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH="src"
```

### Optional PostgreSQL setup

Create a database:

```sql
CREATE DATABASE consumer_brand_intel;
```

Run the schema:

```powershell
psql -d consumer_brand_intel -f sql/schema.sql
```

## Usage

### 1. Run the ETL pipeline

```powershell
$env:PYTHONPATH="src"
python -m consumer_brand_intel.etl_pipeline `
  --input data/raw/startup_funding_sample.csv `
  --output-dir data/processed
```

### 2. Optional: run ETL and load PostgreSQL

```powershell
$env:PYTHONPATH="src"
python -m consumer_brand_intel.etl_pipeline `
  --input data/raw/startup_funding_sample.csv `
  --output-dir data/processed `
  --database-url "postgresql://user:password@localhost:5432/consumer_brand_intel"
```

### 3. Generate startup rankings

```powershell
$env:PYTHONPATH="src"
python -m consumer_brand_intel.startup_scoring `
  --processed-dir data/processed `
  --output outputs/top_50_startups.csv
```

### 4. Generate forecasts

```powershell
$env:PYTHONPATH="src"
python -m consumer_brand_intel.forecasting `
  --processed-dir data/processed `
  --output-dir outputs `
  --periods 12
```

### 5. Generate an investment memo

```powershell
$env:PYTHONPATH="src"
python -m consumer_brand_intel.investment_memo_generator `
  --company-name "GlowNest" `
  --processed-dir data/processed `
  --rankings-path outputs/top_50_startups.csv `
  --output outputs/glownest_investment_memo.md
```

### 6. Open notebooks

```powershell
jupyter notebook notebooks
```

Recommended notebook order:

1. `01_data_cleaning.ipynb`
2. `02_exploratory_analysis.ipynb`
3. `03_startup_scoring.ipynb`
4. `04_forecasting.ipynb`

### 7. Build the Power BI dashboard

1. Open Power BI Desktop.
2. Import CSVs from `data/processed` and `outputs`, or connect to PostgreSQL.
3. Create relationships described in `powerbi/dashboard_spec.md`.
4. Add the DAX measures from `powerbi/dashboard_spec.md`.
5. Build the six dashboard pages.
6. Export screenshots into `docs/screenshots/`.

### 8. Run tests

```powershell
python -m pytest -q
```

## Conclusion

This project demonstrates how an investment analytics platform can move from raw market data to decision-ready outputs. It includes the engineering foundation of an ETL pipeline and SQL schema, the analytical depth of sector and investor analysis, the quantitative reasoning of ranking and forecasting models, and the business communication layer of Power BI dashboards and investment memos.

The platform is intentionally transparent. Every assumption, calculation, and model choice can be inspected and improved. With real data feeds, richer company metrics, automated orchestration, and production BI deployment, this project could evolve from a portfolio demonstration into a practical market intelligence system for consumer investment teams.

