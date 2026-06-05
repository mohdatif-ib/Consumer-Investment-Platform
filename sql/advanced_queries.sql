-- Top funded sectors
SELECT
    s.sector,
    COUNT(DISTINCT s.startup_id) AS startup_count,
    COUNT(fr.round_id) AS funding_rounds,
    SUM(fr.amount) AS total_funding,
    AVG(fr.amount) AS average_deal_size
FROM startups s
JOIN funding_rounds fr ON s.startup_id = fr.startup_id
GROUP BY s.sector
ORDER BY total_funding DESC;

-- Top funded cities
SELECT
    s.city,
    COUNT(DISTINCT s.startup_id) AS startup_count,
    SUM(fr.amount) AS total_funding,
    AVG(fr.amount) AS average_deal_size
FROM startups s
JOIN funding_rounds fr ON s.startup_id = fr.startup_id
GROUP BY s.city
ORDER BY total_funding DESC;

-- Most active investors
SELECT
    i.investor_name,
    COUNT(DISTINCT inv.startup_id) AS portfolio_startups,
    COUNT(DISTINCT inv.round_id) AS participated_rounds,
    SUM(inv.amount) AS total_invested
FROM investors i
JOIN investments inv ON i.investor_id = inv.investor_id
GROUP BY i.investor_name
ORDER BY participated_rounds DESC, total_invested DESC;

-- Average deal size by funding stage
SELECT
    funding_stage,
    COUNT(*) AS rounds,
    AVG(amount) AS average_deal_size,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) AS median_deal_size
FROM funding_rounds
GROUP BY funding_stage
ORDER BY average_deal_size DESC;

-- Funding growth by year
WITH annual_funding AS (
    SELECT
        EXTRACT(YEAR FROM funding_date)::INTEGER AS funding_year,
        SUM(amount) AS total_funding
    FROM funding_rounds
    GROUP BY EXTRACT(YEAR FROM funding_date)
)
SELECT
    funding_year,
    total_funding,
    LAG(total_funding) OVER (ORDER BY funding_year) AS prior_year_funding,
    ROUND(
        100.0 * (total_funding - LAG(total_funding) OVER (ORDER BY funding_year))
        / NULLIF(LAG(total_funding) OVER (ORDER BY funding_year), 0),
        2
    ) AS yoy_growth_pct
FROM annual_funding
ORDER BY funding_year;

-- Startup funding history
SELECT
    s.company_name,
    s.sector,
    s.city,
    fr.funding_date,
    fr.funding_stage,
    fr.amount,
    SUM(fr.amount) OVER (
        PARTITION BY s.startup_id
        ORDER BY fr.funding_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_funding
FROM startups s
JOIN funding_rounds fr ON s.startup_id = fr.startup_id
ORDER BY s.company_name, fr.funding_date;

-- Investor-sector concentration
SELECT
    i.investor_name,
    s.sector,
    COUNT(DISTINCT s.startup_id) AS startups_backed,
    SUM(inv.amount) AS invested_amount
FROM investments inv
JOIN investors i ON inv.investor_id = i.investor_id
JOIN startups s ON inv.startup_id = s.startup_id
GROUP BY i.investor_name, s.sector
ORDER BY i.investor_name, invested_amount DESC;

