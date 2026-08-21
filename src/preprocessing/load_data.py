"""
Data loading & validation for the Olist dataset.

Usage:
    from src.preprocessing.load_data import load_all_tables
    tables = load_all_tables()
    tables["orders"].head()

Design intent (per project guidelines, Section 9 - Phase A):
- Load every raw CSV.
- Parse date columns explicitly.
- Report shape, dtypes, missing values, and duplicate counts per table.
- Confirm the "grain" (what one row represents) for each table BEFORE any
  merging happens elsewhere in the pipeline -- this file does NOT merge tables.
"""
from pathlib import Path
import pandas as pd

from src.config import DATA_RAW, RAW_FILES

# Columns that should be parsed as datetimes per table
DATE_COLUMNS = {
    "orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_items": ["shipping_limit_date"],
    "reviews": ["review_creation_date", "review_answer_timestamp"],
}

# Expected grain key(s) for each table -- used to sanity-check duplicates
GRAIN_KEYS = {
    "customers": ["customer_id"],
    "orders": ["order_id"],
    "order_items": ["order_id", "order_item_id"],
    "products": ["product_id"],
    "payments": None,  # order_id repeats legitimately (multiple installments/methods)
    "reviews": None,   # order_id can repeat/be missing; not a strict 1:1 key
    "sellers": ["seller_id"],
    "geolocation": None,  # zip_code_prefix repeats by design; needs aggregation
    "category_translation": ["product_category_name"],
}


def _check_file_exists(path: Path, friendly_name: str) -> None:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing '{friendly_name}' at {path}.\n"
            f"Download the Olist dataset from Kaggle and place all CSVs in {path.parent}.\n"
            f"See README.md 'Getting the data' section for the exact steps."
        )


def load_all_tables(raw_dir: Path = DATA_RAW, verbose: bool = True) -> dict[str, pd.DataFrame]:
    """Load all Olist CSVs into a dict of DataFrames, with date parsing and a
    validation report. Raises a clear error naming the missing file if any
    CSV has not been downloaded yet."""
    tables: dict[str, pd.DataFrame] = {}

    for key, filename in RAW_FILES.items():
        path = raw_dir / filename
        _check_file_exists(path, filename)

        parse_dates = DATE_COLUMNS.get(key)
        df = pd.read_csv(path, parse_dates=parse_dates)
        tables[key] = df

        if verbose:
            _report_table(key, df)

    return tables


def _report_table(key: str, df: pd.DataFrame) -> None:
    n_rows, n_cols = df.shape
    n_dupes = df.duplicated().sum()
    grain = GRAIN_KEYS.get(key)
    grain_note = ""
    if grain:
        n_grain_dupes = df.duplicated(subset=grain).sum()
        grain_note = f" | duplicate rows on grain key {grain}: {n_grain_dupes}"

    n_missing_cols = (df.isna().sum() > 0).sum()

    print(
        f"[{key:22s}] rows={n_rows:>7,} cols={n_cols:>2} "
        f"exact_dupes={n_dupes:>5} cols_with_missing={n_missing_cols:>2}{grain_note}"
    )


if __name__ == "__main__":
    print("Loading and validating all Olist tables...\n")
    loaded = load_all_tables()
    print(f"\nLoaded {len(loaded)} tables successfully.")
