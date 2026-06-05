# Power BI Dashboard Specification

## Data Model

Import these tables from PostgreSQL or `data/processed/*.csv`:

- `startups`
- `funding_rounds`
- `investors`
- `investments`
- `funding_events`
- `top_50_startups`
- `funding_forecasts`
- `fastest_growing_sectors`

Relationships:

- `startups[startup_id]` 1:* `funding_rounds[startup_id]`
- `startups[startup_id]` 1:* `investments[startup_id]`
- `investors[investor_id]` 1:* `investments[investor_id]`
- `funding_rounds[round_id]` 1:* `investments[round_id]`

## DAX Measures

```DAX
Total Funding = SUM(funding_rounds[amount])

Total Startups = DISTINCTCOUNT(startups[startup_id])

Total Investors = DISTINCTCOUNT(investors[investor_id])

Number of Funding Rounds = DISTINCTCOUNT(funding_rounds[round_id])

Average Deal Size = DIVIDE([Total Funding], [Number of Funding Rounds])

Median Deal Size =
MEDIAN(funding_rounds[amount])

Funding YoY Growth =
VAR CurrentYearFunding = [Total Funding]
VAR PriorYearFunding =
    CALCULATE(
        [Total Funding],
        DATEADD(funding_rounds[funding_date], -1, YEAR)
    )
RETURN
    DIVIDE(CurrentYearFunding - PriorYearFunding, PriorYearFunding)

Investor Participation = DISTINCTCOUNT(investments[round_id])

Investor Total Invested = SUM(investments[amount])

Average Investor Check Size = DIVIDE([Investor Total Invested], COUNTROWS(investments))

Sector Funding Rank =
RANKX(
    ALL(startups[sector]),
    [Total Funding],
    ,
    DESC,
    Dense
)

City Funding Rank =
RANKX(
    ALL(startups[city]),
    [Total Funding],
    ,
    DESC,
    Dense
)

Top Opportunity Score =
MAX(top_50_startups[investment_attractiveness_score])

Forecasted Funding = SUM(funding_forecasts[predicted_funding])

Funding Per Startup = DIVIDE([Total Funding], [Total Startups])
```

## Page 1: Executive Overview

Purpose: give partners a fast read on market size, deal velocity, and capital concentration.

Visuals:

- KPI cards: Total Funding, Total Startups, Total Investors, Average Deal Size
- Line chart: funding over time by month
- Bar chart: top sectors by total funding
- Matrix: top 10 startups by total funding and latest funding stage
- Slicers: sector, city, funding stage, funding year

## Page 2: Sector Analysis

Visuals:

- Clustered bar chart: funding by sector
- Line chart: sector growth by year
- Matrix: sector, startup count, total funding, average deal size, YoY growth
- Tooltip page: top startups and active investors for selected sector

## Page 3: Investor Analysis

Visuals:

- Bar chart: top investors by participated rounds
- Scatter plot: total invested vs portfolio startup count
- Matrix: investor, sector, invested amount, startups backed
- Donut chart: investor participation by funding stage

## Page 4: Geographic Analysis

Visuals:

- Map: funding by city
- Bar chart: top funded cities
- Matrix: city, sector, total funding, startup count, average deal size

## Page 5: Investment Opportunities

Visuals:

- Table: top startup rankings with score components
- Bar chart: investment attractiveness score by startup
- Decomposition tree: attractiveness score by sector, city, funding stage
- Detail panel: funding history and investor list for selected startup

## Page 6: Forecasting

Visuals:

- Line chart: historical and forecasted funding by month
- Small multiples: forecast model comparison
- Table: fastest growing sectors
- KPI cards: next 12 months forecasted funding, highest growth sector

## Design Notes

- Use a clean institutional palette: charcoal text, white canvas, muted teal for primary funding measures, gold for opportunity scores, slate for neutral trend context.
- Use currency formatting in USD with compact units.
- Keep slicers synced across all analysis pages.
- Add drill-through from startup tables to a startup detail page if expanding beyond the six requested pages.

