"""VC-style startup scoring model.

Scoring weights:
- Funding Growth: 40%
- Investor Quality: 30%
- Sector Growth: 20%
- Funding Consistency: 10%
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from sklearn.preprocessing import MinMaxScaler
except ImportError:  # pragma: no cover - local fallback for lean environments
    MinMaxScaler = None


WEIGHTS = {
    "funding_growth_score": 0.40,
    "investor_quality_score": 0.30,
    "sector_growth_score": 0.20,
    "funding_consistency_score": 0.10,
}


def _safe_growth(values: pd.Series) -> float:
    values = values.sort_index()
    if len(values) < 2:
        return 0.0
    previous = values.iloc[-2]
    current = values.iloc[-1]
    if previous <= 0:
        return 0.0
    return float((current - previous) / previous)


def _normalize(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    normalized = df.copy()
    if normalized.empty:
        return normalized
    values = normalized[columns].fillna(0)
    if MinMaxScaler is not None:
        scaler = MinMaxScaler()
        normalized[columns] = scaler.fit_transform(values)
    else:
        denominator = values.max() - values.min()
        normalized[columns] = (values - values.min()) / denominator.replace(0, 1)
    return normalized


def build_scoring_features(
    funding_events: pd.DataFrame,
    investments: pd.DataFrame,
    investors: pd.DataFrame,
) -> pd.DataFrame:
    """Engineer startup, investor, and sector features for ranking."""

    events = funding_events.copy()
    events["funding_date"] = pd.to_datetime(events["funding_date"])
    events["year"] = events["funding_date"].dt.year

    annual_by_startup = (
        events.groupby(["startup_id", "year"])["amount_usd"].sum().reset_index()
    )
    startup_growth = annual_by_startup.groupby("startup_id").apply(
        lambda group: _safe_growth(group.set_index("year")["amount_usd"]),
        include_groups=False,
    )

    annual_by_sector = events.groupby(["sector", "year"])["amount_usd"].sum().reset_index()
    sector_growth = annual_by_sector.groupby("sector").apply(
        lambda group: _safe_growth(group.set_index("year")["amount_usd"]),
        include_groups=False,
    )

    investor_reputation = (
        investments.merge(investors, on="investor_id", how="left")
        .groupby("investor_id")
        .agg(
            investor_total_amount=("amount", "sum"),
            investor_rounds=("round_id", "nunique"),
            investor_startups=("startup_id", "nunique"),
        )
        .reset_index()
    )
    investor_reputation["investor_quality"] = (
        np.log1p(investor_reputation["investor_total_amount"])
        + investor_reputation["investor_rounds"]
        + investor_reputation["investor_startups"]
    )

    startup_investor_quality = (
        investments.merge(investor_reputation[["investor_id", "investor_quality"]], on="investor_id", how="left")
        .groupby("startup_id")["investor_quality"]
        .mean()
    )

    base = (
        events.groupby("startup_id")
        .agg(
            company_name=("company_name", "first"),
            sector=("sector", "first"),
            city=("city", "first"),
            total_funding=("amount_usd", "sum"),
            average_deal_size=("amount_usd", "mean"),
            funding_rounds=("event_id", "nunique"),
            first_funding_date=("funding_date", "min"),
            latest_funding_date=("funding_date", "max"),
            funding_std=("amount_usd", "std"),
        )
        .reset_index()
    )

    base["funding_growth"] = base["startup_id"].map(startup_growth).fillna(0)
    base["sector_growth"] = base["sector"].map(sector_growth).fillna(0)
    base["investor_quality"] = base["startup_id"].map(startup_investor_quality).fillna(0)
    base["funding_consistency"] = 1 / (1 + (base["funding_std"].fillna(0) / base["average_deal_size"].replace(0, np.nan)).fillna(0))

    return base


def score_startups(features: pd.DataFrame) -> pd.DataFrame:
    """Normalize features and calculate weighted attractiveness score."""

    scored = features.copy()
    raw_to_score = {
        "funding_growth": "funding_growth_score",
        "investor_quality": "investor_quality_score",
        "sector_growth": "sector_growth_score",
        "funding_consistency": "funding_consistency_score",
    }
    scored = scored.rename(columns=raw_to_score)
    scored = _normalize(scored, list(raw_to_score.values()))

    scored["investment_attractiveness_score"] = sum(
        scored[column] * weight for column, weight in WEIGHTS.items()
    )
    scored["investment_attractiveness_score"] = (scored["investment_attractiveness_score"] * 100).round(2)
    scored = scored.sort_values(
        ["investment_attractiveness_score", "total_funding"],
        ascending=[False, False],
    ).reset_index(drop=True)
    scored.insert(0, "rank", np.arange(1, len(scored) + 1))
    return scored


def rank_startups(processed_dir: Path, output_path: Path, top_n: int = 50) -> pd.DataFrame:
    """Load processed ETL output and write top startup rankings."""

    funding_events = pd.read_csv(processed_dir / "funding_events.csv")
    investments = pd.read_csv(processed_dir / "investments.csv")
    investors = pd.read_csv(processed_dir / "investors.csv")

    features = build_scoring_features(funding_events, investments, investors)
    scored = score_startups(features).head(top_n)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    scored.to_csv(output_path, index=False)
    return scored


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rank startups by VC investment attractiveness.")
    parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--output", type=Path, default=Path("outputs/top_50_startups.csv"))
    parser.add_argument("--top-n", type=int, default=50)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rankings = rank_startups(args.processed_dir, args.output, args.top_n)
    print(rankings[["rank", "company_name", "sector", "investment_attractiveness_score"]].to_string(index=False))


if __name__ == "__main__":
    main()
