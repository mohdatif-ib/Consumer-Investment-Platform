"""AI-style investment memo generator.

This module is intentionally deterministic so it can run without external API
keys. It creates a structured investment memo from startup context, funding
history, sector, and optional ranking score.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


HIGH_GROWTH_SECTORS = {
    "Beauty & Personal Care",
    "Food & Beverage",
    "Health & Wellness",
    "Pet Care",
}


@dataclass
class InvestmentMemo:
    company_name: str
    investment_thesis: str
    risks: list[str]
    opportunities: list[str]
    recommendation_score: float
    recommendation: str

    def to_markdown(self) -> str:
        risks = "\n".join(f"- {risk}" for risk in self.risks)
        opportunities = "\n".join(f"- {opportunity}" for opportunity in self.opportunities)
        return f"""# Investment Memo: {self.company_name}

## Investment Thesis
{self.investment_thesis}

## Opportunities
{opportunities}

## Risks
{risks}

## Recommendation
Score: {self.recommendation_score:.1f}/100

{self.recommendation}
"""


def generate_memo(
    company_name: str,
    startup_description: str,
    sector: str,
    funding_history: pd.DataFrame,
    ranking_score: float | None = None,
) -> InvestmentMemo:
    """Generate a VC-style investment memo."""

    history = funding_history.copy()
    history["funding_date"] = pd.to_datetime(history["funding_date"])
    history = history.sort_values("funding_date")
    total_funding = history["amount_usd"].sum()
    round_count = history["funding_stage"].nunique()
    latest_stage = history["funding_stage"].iloc[-1] if not history.empty else "Unknown"

    if len(history) >= 2 and history["amount_usd"].iloc[-2] > 0:
        growth = (history["amount_usd"].iloc[-1] - history["amount_usd"].iloc[-2]) / history["amount_usd"].iloc[-2]
    else:
        growth = 0.0

    base_score = ranking_score if ranking_score is not None else 50
    growth_bonus = min(max(growth * 15, -10), 15)
    sector_bonus = 8 if sector in HIGH_GROWTH_SECTORS else 3
    stage_bonus = 6 if latest_stage in {"Series B", "Series C", "Growth"} else 2
    recommendation_score = max(0, min(100, base_score + growth_bonus + sector_bonus + stage_bonus))

    description = startup_description.rstrip(".")
    thesis = (
        f"{company_name} operates in {sector} with a product narrative centered on "
        f"{description}. The company has raised "
        f"${total_funding:,.0f} across {round_count} disclosed funding stage(s), with the latest "
        f"round at {latest_stage}. Its funding trajectory suggests "
        f"{'accelerating investor demand' if growth > 0.2 else 'a developing capital formation pattern'}."
    )

    opportunities = [
        "Expand omnichannel distribution across retail, marketplace, and direct-to-consumer channels.",
        "Use customer cohort data to improve repeat purchase, retention, and margin quality.",
        "Leverage category momentum and investor syndicate support to access follow-on capital.",
    ]
    if sector in HIGH_GROWTH_SECTORS:
        opportunities.append("Category tailwinds create room for premium positioning and rapid brand awareness gains.")

    risks = [
        "Consumer brand demand may weaken if customer acquisition costs rise or repeat purchase slows.",
        "Competitive products can pressure pricing power, shelf access, and gross margin.",
        "Funding momentum alone does not prove unit economics, retention quality, or operational scalability.",
    ]
    if growth < 0:
        risks.append("Latest disclosed funding declined versus the prior round, which may indicate valuation or traction pressure.")

    recommendation = (
        "Prioritize for partner review and deeper diligence."
        if recommendation_score >= 75
        else "Track closely and request additional financial, cohort, and channel data."
        if recommendation_score >= 55
        else "Keep in market map unless additional traction evidence emerges."
    )

    return InvestmentMemo(company_name, thesis, risks, opportunities, recommendation_score, recommendation)


def memo_from_processed_data(company_name: str, processed_dir: Path, rankings_path: Path | None = None) -> InvestmentMemo:
    events = pd.read_csv(processed_dir / "funding_events.csv", parse_dates=["funding_date"])
    company_events = events[events["company_name"].str.lower() == company_name.lower()]
    if company_events.empty:
        raise ValueError(f"No processed funding history found for {company_name}")

    ranking_score = None
    if rankings_path and rankings_path.exists():
        rankings = pd.read_csv(rankings_path)
        match = rankings[rankings["company_name"].str.lower() == company_name.lower()]
        if not match.empty:
            ranking_score = float(match["investment_attractiveness_score"].iloc[0])

    first = company_events.iloc[0]
    return generate_memo(
        company_name=first["company_name"],
        startup_description=first.get("startup_description", ""),
        sector=first["sector"],
        funding_history=company_events,
        ranking_score=ranking_score,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a VC investment memo.")
    parser.add_argument("--company-name", required=True)
    parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--rankings-path", type=Path, default=Path("outputs/top_50_startups.csv"))
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    memo = memo_from_processed_data(args.company_name, args.processed_dir, args.rankings_path)
    markdown = memo.to_markdown()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
    print(markdown)


if __name__ == "__main__":
    main()
