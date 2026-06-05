-- Consumer Brand Investment Intelligence Platform
-- PostgreSQL schema for normalized startup funding analytics.

DROP TABLE IF EXISTS investments CASCADE;
DROP TABLE IF EXISTS funding_rounds CASCADE;
DROP TABLE IF EXISTS investors CASCADE;
DROP TABLE IF EXISTS startups CASCADE;

CREATE TABLE startups (
    startup_id INTEGER PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL UNIQUE,
    sector VARCHAR(150) NOT NULL,
    city VARCHAR(150) NOT NULL,
    founded_year INTEGER CHECK (founded_year BETWEEN 1900 AND EXTRACT(YEAR FROM CURRENT_DATE)::INTEGER + 1),
    startup_description TEXT
);

CREATE TABLE funding_rounds (
    round_id INTEGER PRIMARY KEY,
    startup_id INTEGER NOT NULL REFERENCES startups(startup_id),
    funding_date DATE NOT NULL,
    funding_stage VARCHAR(100) NOT NULL,
    amount NUMERIC(18, 2) NOT NULL CHECK (amount >= 0)
);

CREATE TABLE investors (
    investor_id INTEGER PRIMARY KEY,
    investor_name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE investments (
    investment_id INTEGER PRIMARY KEY,
    startup_id INTEGER NOT NULL REFERENCES startups(startup_id),
    investor_id INTEGER NOT NULL REFERENCES investors(investor_id),
    round_id INTEGER REFERENCES funding_rounds(round_id),
    amount NUMERIC(18, 2) NOT NULL CHECK (amount >= 0)
);

CREATE INDEX idx_startups_sector ON startups(sector);
CREATE INDEX idx_startups_city ON startups(city);
CREATE INDEX idx_funding_rounds_date ON funding_rounds(funding_date);
CREATE INDEX idx_funding_rounds_startup ON funding_rounds(startup_id);
CREATE INDEX idx_investments_investor ON investments(investor_id);
CREATE INDEX idx_investments_startup ON investments(startup_id);

