"""
Central configuration for the E-Commerce Customer Intelligence project.
Import paths from here instead of hardcoding strings across notebooks/scripts.
"""
from pathlib import Path

# --- Project root & data locations ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"

# --- Expected raw Olist files (download from Kaggle, see README) ---
RAW_FILES = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "products": "olist_products_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

# --- Table grain notes (read before joining anything!) ---
# customers:            1 row per customer_id (customer_unique_id can repeat across customer_id)
# orders:                1 row per order_id
# order_items:           1 row per (order_id, order_item_id) -- an order can have MULTIPLE rows
# products:               1 row per product_id
# payments:              1+ rows per order_id (an order can have multiple payment installments/methods)
# reviews:                ~1 row per order_id (occasionally duplicated/missing)
# sellers:                 1 row per seller_id
# geolocation:            many rows per zip_code_prefix (not unique -- needs aggregation before joining)

RANDOM_SEED = 42
