"""Command-line ETL pipeline for the investment intelligence platform."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from consumer_brand_intel.data_cleaning import CleanedTables, clean_csv_files


LOGGER = logging.getLogger(__name__)


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def load_tables_to_postgres(tables: CleanedTables, database_url: str) -> None:
    """Load cleaned tables into PostgreSQL using SQLAlchemy."""

    try:
        from sqlalchemy import create_engine
    except ImportError as exc:
        raise RuntimeError(
            "PostgreSQL loading requires SQLAlchemy. Install project dependencies with "
            "`pip install -r requirements.txt`."
        ) from exc

    engine = create_engine(database_url)
    table_order = ["startups", "funding_rounds", "investors", "investments", "funding_events", "metrics"]
    for table_name in table_order:
        table = getattr(tables, table_name)
        LOGGER.info("Loading %s rows into %s", len(table), table_name)
        table.to_sql(table_name, engine, if_exists="replace", index=False)


def run_etl(input_files: list[Path], output_dir: Path, database_url: str | None = None) -> CleanedTables:
    """Run the full CSV-to-analytics-table ETL process."""

    LOGGER.info("Starting ETL for %s input file(s)", len(input_files))
    tables = clean_csv_files(input_files, output_dir)
    LOGGER.info("Cleaned tables saved to %s", output_dir)

    if database_url:
        load_tables_to_postgres(tables, database_url)
        LOGGER.info("PostgreSQL load complete")

    return tables


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run startup funding ETL pipeline.")
    parser.add_argument(
        "--input",
        nargs="+",
        type=Path,
        default=[Path("data/raw/startup_funding_sample.csv")],
        help="One or more raw CSV files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed"),
        help="Directory where cleaned CSV tables will be written.",
    )
    parser.add_argument(
        "--database-url",
        default=None,
        help="Optional PostgreSQL SQLAlchemy URL, e.g. postgresql://user:password@localhost:5432/db",
    )
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    run_etl(args.input, args.output_dir, args.database_url)


if __name__ == "__main__":
    main()
