"""Data cleaning utilities for startup funding datasets.

The module converts raw CSV files into normalized analytical tables used by
the SQL load, notebooks, scoring model, and Power BI dashboard.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "company_name",
    "sector",
    "city",
    "founded_year",
    "funding_date",
    "funding_stage",
    "amount",
    "currency",
    "investors",
}

DEFAULT_EXCHANGE_RATES_TO_USD = {
    "USD": 1.00,
    "EUR": 1.08,
    "GBP": 1.27,
    "INR": 0.012,
    "CAD": 0.73,
    "AUD": 0.66,
}


@dataclass(frozen=True)
class CleanedTables:
    """Container for normalized analytical tables."""

    startups: pd.DataFrame
    funding_rounds: pd.DataFrame
    investors: pd.DataFrame
    investments: pd.DataFrame
    funding_events: pd.DataFrame
    metrics: pd.DataFrame


def load_csv_files(input_paths: Iterable[str | Path]) -> pd.DataFrame:
    """Load one or more raw funding CSV files into a single DataFrame."""

    frames: list[pd.DataFrame] = []
    for input_path in input_paths:
        path = Path(input_path)
        if not path.exists():
            raise FileNotFoundError(f"Input file does not exist: {path}")
        frames.append(pd.read_csv(path))

    if not frames:
        raise ValueError("At least one CSV file is required.")

    return pd.concat(frames, ignore_index=True)


def _normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = (
        cleaned.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return cleaned


def validate_schema(df: pd.DataFrame) -> None:
    """Validate required raw data fields."""

    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def parse_money(value: object) -> float:
    """Parse currency strings such as '$1.2M' or numeric values to float."""

    if pd.isna(value):
        return np.nan
    if isinstance(value, (int, float, np.number)):
        return float(value)

    text = str(value).strip().replace(",", "")
    multiplier = 1.0
    if text.upper().endswith("M"):
        multiplier = 1_000_000.0
        text = text[:-1]
    elif text.upper().endswith("B"):
        multiplier = 1_000_000_000.0
        text = text[:-1]
    elif text.upper().endswith("K"):
        multiplier = 1_000.0
        text = text[:-1]

    text = text.replace("$", "").replace("€", "").replace("£", "").replace("₹", "")
    return float(text) * multiplier


def clean_raw_funding_data(
    df: pd.DataFrame,
    exchange_rates_to_usd: dict[str, float] | None = None,
) -> pd.DataFrame:
    """Clean missing values, duplicates, dates, text, and currency amounts."""

    exchange_rates = exchange_rates_to_usd or DEFAULT_EXCHANGE_RATES_TO_USD
    cleaned = _normalize_column_names(df)
    validate_schema(cleaned)
    if "startup_description" not in cleaned.columns:
        cleaned["startup_description"] = ""

    text_columns = ["company_name", "sector", "city", "funding_stage", "currency", "investors", "startup_description"]
    for column in text_columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()

    cleaned["company_name"] = cleaned["company_name"].str.replace(r"\s+", " ", regex=True)
    cleaned["sector"] = cleaned["sector"].fillna("Unknown").str.title()
    cleaned["city"] = cleaned["city"].fillna("Unknown").str.title()
    cleaned["funding_stage"] = cleaned["funding_stage"].fillna("Unknown").str.title()
    cleaned["currency"] = cleaned["currency"].fillna("USD").str.upper()
    cleaned["investors"] = cleaned["investors"].fillna("Undisclosed")

    cleaned["founded_year"] = pd.to_numeric(cleaned["founded_year"], errors="coerce")
    median_year = int(cleaned["founded_year"].dropna().median()) if cleaned["founded_year"].notna().any() else 2020
    cleaned["founded_year"] = cleaned["founded_year"].fillna(median_year).astype(int)

    cleaned["funding_date"] = pd.to_datetime(cleaned["funding_date"], errors="coerce")
    cleaned = cleaned.dropna(subset=["company_name", "funding_date"])

    cleaned["amount"] = cleaned["amount"].apply(parse_money)
    cleaned["amount"] = cleaned["amount"].fillna(cleaned["amount"].median())
    cleaned["exchange_rate_to_usd"] = cleaned["currency"].map(exchange_rates).fillna(1.0)
    cleaned["amount_usd"] = (cleaned["amount"] * cleaned["exchange_rate_to_usd"]).round(2)

    dedupe_columns = ["company_name", "funding_date", "funding_stage", "amount_usd"]
    cleaned = cleaned.drop_duplicates(subset=dedupe_columns, keep="first")
    cleaned = cleaned.sort_values(["funding_date", "company_name"]).reset_index(drop=True)
    cleaned["event_id"] = np.arange(1, len(cleaned) + 1)

    return cleaned


def build_analytical_tables(cleaned: pd.DataFrame) -> CleanedTables:
    """Build dimensional tables and bridge tables for SQL/BI analysis."""

    startups = (
        cleaned[["company_name", "sector", "city", "founded_year", "startup_description"]]
        .drop_duplicates(subset=["company_name"])
        .sort_values("company_name")
        .reset_index(drop=True)
    )
    startups.insert(0, "startup_id", np.arange(1, len(startups) + 1))

    company_to_id = dict(zip(startups["company_name"], startups["startup_id"]))

    funding_rounds = cleaned[
        ["event_id", "company_name", "funding_date", "funding_stage", "amount_usd"]
    ].copy()
    funding_rounds = funding_rounds.rename(columns={"event_id": "round_id", "amount_usd": "amount"})
    funding_rounds["startup_id"] = funding_rounds["company_name"].map(company_to_id)
    funding_rounds = funding_rounds[
        ["round_id", "startup_id", "funding_date", "funding_stage", "amount"]
    ]

    investor_names = sorted(
        {
            investor.strip()
            for investors in cleaned["investors"].fillna("Undisclosed")
            for investor in str(investors).split(";")
            if investor.strip()
        }
    )
    investors = pd.DataFrame(
        {
            "investor_id": np.arange(1, len(investor_names) + 1),
            "investor_name": investor_names,
        }
    )
    investor_to_id = dict(zip(investors["investor_name"], investors["investor_id"]))

    investment_rows: list[dict[str, object]] = []
    investment_id = 1
    for _, row in cleaned.iterrows():
        row_investors = [name.strip() for name in str(row["investors"]).split(";") if name.strip()]
        if not row_investors:
            row_investors = ["Undisclosed"]
        split_amount = float(row["amount_usd"]) / len(row_investors)
        for investor in row_investors:
            investment_rows.append(
                {
                    "investment_id": investment_id,
                    "startup_id": company_to_id[row["company_name"]],
                    "investor_id": investor_to_id[investor],
                    "round_id": int(row["event_id"]),
                    "amount": round(split_amount, 2),
                }
            )
            investment_id += 1

    investments = pd.DataFrame(investment_rows)
    funding_events = cleaned.merge(startups[["startup_id", "company_name"]], on="company_name", how="left")
    metrics = calculate_platform_metrics(funding_events)

    return CleanedTables(
        startups=startups,
        funding_rounds=funding_rounds,
        investors=investors,
        investments=investments,
        funding_events=funding_events,
        metrics=metrics,
    )


def calculate_platform_metrics(funding_events: pd.DataFrame) -> pd.DataFrame:
    """Calculate portfolio-level metrics requested for the platform."""

    investor_count = len(
        {
            investor.strip()
            for investors in funding_events["investors"].fillna("")
            for investor in str(investors).split(";")
            if investor.strip()
        }
    )
    annual_funding = (
        funding_events.assign(year=funding_events["funding_date"].dt.year)
        .groupby("year")["amount_usd"]
        .sum()
        .sort_index()
    )
    latest_growth = annual_funding.pct_change().replace([np.inf, -np.inf], np.nan).iloc[-1]

    metrics = {
        "total_funding": funding_events["amount_usd"].sum(),
        "average_deal_size": funding_events["amount_usd"].mean(),
        "funding_growth_latest_year_pct": 0 if pd.isna(latest_growth) else latest_growth * 100,
        "number_of_investors": investor_count,
        "number_of_funding_rounds": funding_events["event_id"].nunique(),
    }
    return pd.DataFrame([metrics]).round(2)


def save_cleaned_tables(tables: CleanedTables, output_dir: str | Path) -> None:
    """Persist analytical tables as CSV files."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    for name, table in tables.__dict__.items():
        path = output_path / f"{name}.csv"
        table.to_csv(path, index=False)


def clean_csv_files(input_paths: Iterable[str | Path], output_dir: str | Path) -> CleanedTables:
    """Load, clean, normalize, and save startup funding CSV files."""

    raw = load_csv_files(input_paths)
    cleaned = clean_raw_funding_data(raw)
    tables = build_analytical_tables(cleaned)
    save_cleaned_tables(tables, output_dir)
    return tables
