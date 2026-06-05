from pathlib import Path

from consumer_brand_intel.data_cleaning import clean_csv_files
from consumer_brand_intel.startup_scoring import build_scoring_features, score_startups


def test_clean_csv_files_builds_expected_tables(tmp_path):
    raw_path = Path("data/raw/startup_funding_sample.csv")

    tables = clean_csv_files([raw_path], tmp_path)

    assert not tables.startups.empty
    assert not tables.funding_rounds.empty
    assert not tables.investors.empty
    assert not tables.investments.empty
    assert tables.metrics.loc[0, "number_of_funding_rounds"] == len(tables.funding_rounds)
    assert (tmp_path / "funding_events.csv").exists()


def test_scoring_returns_ranked_startups(tmp_path):
    raw_path = Path("data/raw/startup_funding_sample.csv")
    tables = clean_csv_files([raw_path], tmp_path)

    features = build_scoring_features(tables.funding_events, tables.investments, tables.investors)
    rankings = score_startups(features)

    assert rankings["rank"].is_monotonic_increasing
    assert rankings["investment_attractiveness_score"].between(0, 100).all()
    assert rankings.iloc[0]["investment_attractiveness_score"] >= rankings.iloc[-1]["investment_attractiveness_score"]

