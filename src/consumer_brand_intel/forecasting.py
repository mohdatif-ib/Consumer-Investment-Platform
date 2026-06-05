"""Forecast future startup funding activity by month and sector."""

from __future__ import annotations

import argparse
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from sklearn.linear_model import LinearRegression
except ImportError:  # pragma: no cover - local fallback for lean environments
    LinearRegression = None

try:
    from statsmodels.tsa.arima.model import ARIMA
except ImportError:  # pragma: no cover - optional dependency fallback
    ARIMA = None


def load_monthly_funding(funding_events_path: Path) -> pd.DataFrame:
    events = pd.read_csv(funding_events_path, parse_dates=["funding_date"])
    monthly = (
        events.set_index("funding_date")
        .resample("MS")["amount_usd"]
        .sum()
        .rename("monthly_funding")
        .reset_index()
    )
    monthly["month_index"] = np.arange(len(monthly))
    return monthly


def forecast_with_linear_regression(monthly: pd.DataFrame, periods: int = 12) -> pd.DataFrame:
    x = monthly[["month_index"]]
    y = monthly["monthly_funding"]

    future_index = np.arange(len(monthly), len(monthly) + periods)
    future_dates = pd.date_range(
        monthly["funding_date"].max() + pd.offsets.MonthBegin(1),
        periods=periods,
        freq="MS",
    )
    if LinearRegression is not None:
        model = LinearRegression()
        model.fit(x, y)
        predictions = model.predict(future_index.reshape(-1, 1))
    else:
        slope, intercept = np.polyfit(monthly["month_index"], y, deg=1)
        predictions = slope * future_index + intercept

    return pd.DataFrame(
        {
            "forecast_month": future_dates,
            "model": "Linear Regression",
            "predicted_funding": np.maximum(predictions, 0).round(2),
        }
    )


def forecast_with_arima(monthly: pd.DataFrame, periods: int = 12) -> pd.DataFrame:
    future_dates = pd.date_range(
        monthly["funding_date"].max() + pd.offsets.MonthBegin(1),
        periods=periods,
        freq="MS",
    )
    if ARIMA is None or len(monthly) < 8:
        baseline = monthly["monthly_funding"].rolling(3, min_periods=1).mean().iloc[-1]
        predictions = np.repeat(baseline, periods)
        model_name = "ARIMA fallback moving average"
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = ARIMA(monthly["monthly_funding"], order=(1, 1, 1))
            fit = model.fit()
            predictions = fit.forecast(steps=periods)
        model_name = "ARIMA(1,1,1)"

    return pd.DataFrame(
        {
            "forecast_month": future_dates,
            "model": model_name,
            "predicted_funding": np.maximum(predictions, 0).round(2),
        }
    )


def identify_fastest_growing_sectors(funding_events_path: Path) -> pd.DataFrame:
    events = pd.read_csv(funding_events_path, parse_dates=["funding_date"])
    events["year"] = events["funding_date"].dt.year
    sector_year = events.groupby(["sector", "year"])["amount_usd"].sum().reset_index()

    rows: list[dict[str, object]] = []
    for sector, group in sector_year.groupby("sector"):
        group = group.sort_values("year")
        if len(group) < 2:
            growth_rate = 0.0
        else:
            previous = group["amount_usd"].iloc[-2]
            latest = group["amount_usd"].iloc[-1]
            growth_rate = 0.0 if previous <= 0 else (latest - previous) / previous
        rows.append(
            {
                "sector": sector,
                "latest_year": int(group["year"].iloc[-1]),
                "latest_year_funding": float(group["amount_usd"].iloc[-1]),
                "year_over_year_growth_pct": round(growth_rate * 100, 2),
            }
        )

    return pd.DataFrame(rows).sort_values("year_over_year_growth_pct", ascending=False)


def generate_forecasts(processed_dir: Path, output_dir: Path, periods: int = 12) -> tuple[pd.DataFrame, pd.DataFrame]:
    funding_events_path = processed_dir / "funding_events.csv"
    monthly = load_monthly_funding(funding_events_path)
    forecasts = pd.concat(
        [
            forecast_with_linear_regression(monthly, periods),
            forecast_with_arima(monthly, periods),
        ],
        ignore_index=True,
    )
    fastest_sectors = identify_fastest_growing_sectors(funding_events_path)

    output_dir.mkdir(parents=True, exist_ok=True)
    forecasts.to_csv(output_dir / "funding_forecasts.csv", index=False)
    fastest_sectors.to_csv(output_dir / "fastest_growing_sectors.csv", index=False)
    return forecasts, fastest_sectors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Forecast next 12 months of funding activity.")
    parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--periods", type=int, default=12)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    forecasts, sectors = generate_forecasts(args.processed_dir, args.output_dir, args.periods)
    print(forecasts.head(12).to_string(index=False))
    print("\nFastest growing sectors")
    print(sectors.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
