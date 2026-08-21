# E-Commerce Customer Intelligence and Personalized Recommendation System

AI/ML capstone project: an end-to-end pipeline that turns raw Olist e-commerce
transactional data into customer segments, a repeat-purchase prediction model,
a Top-N product recommender, a business dashboard, and (optionally) an API +
GenAI explanation layer.

## 1. Getting the data

The raw CSVs are **not** committed to this repo (see `.gitignore`) — download them yourself:

1. Go to the Kaggle dataset page: **"Brazilian E-Commerce Public Dataset by Olist"**
   (search "olist ecommerce kaggle" — the dataset is published by Olist on Kaggle).
2. Download the ZIP (Kaggle account required) and extract it.
3. Copy all 9 CSVs into `data/raw/`:
   ```
   data/raw/
   ├── olist_customers_dataset.csv
   ├── olist_orders_dataset.csv
   ├── olist_order_items_dataset.csv
   ├── olist_products_dataset.csv
   ├── olist_order_payments_dataset.csv
   ├── olist_order_reviews_dataset.csv
   ├── olist_sellers_dataset.csv
   ├── olist_geolocation_dataset.csv
   └── product_category_name_translation.csv
   ```

Alternative: use the Kaggle CLI if you have an API token set up:
```bash
kaggle datasets download -d olistbr/brazilian-ecommerce -p data/raw --unzip
```

## 2. Environment setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Register the Jupyter kernel (optional but recommended):
```bash
python -m ipykernel install --user --name=ecommerce-ai-ml
```

## 3. Validate the data loads correctly

```bash
python -m src.preprocessing.load_data
```
This loads all 9 tables, parses date columns, and prints row counts, duplicate
counts, and missing-value summaries per table — confirm this runs clean before
writing any cleaning/merge logic. Read the grain notes in `src/config.py`
before joining anything (an order has multiple `order_items` rows; payments
and reviews are not strictly 1:1 with `order_id`).

## 4. Project roadmap (phases from the project guidelines)

| Phase | Description | Location |
|---|---|---|
| A | Data understanding & quality checks | `notebooks/`, `src/preprocessing/` |
| B | EDA & business insights | `notebooks/` |
| C | Customer feature engineering (RFM etc.) | `src/features/` |
| D | Customer segmentation (K-Means) | `src/segmentation/` |
| E | Supervised ML — repeat-purchase prediction | `src/prediction/` |
| F | Product recommendation engine | `src/recommendation/` |
| Optional | Review sentiment (NLP) | `src/nlp/` |
| Optional | Recommendation/insight explanations (GenAI) | `src/genai/` |
| — | Business dashboard | `dashboard/` (Power BI) |
| Optional | Model serving | `api/` (FastAPI) |

Status: **project scaffolding complete — data download + Phase A next.**

## 5. Folder structure

```
ecommerce-ai-ml-project/
├── data/
│   ├── raw/            # untouched CSVs from Kaggle (gitignored)
│   └── processed/      # cleaned/merged analytical tables (gitignored)
├── notebooks/           # EDA and exploratory work
├── sql/                 # business queries against the cleaned tables
├── src/
│   ├── config.py         # paths, constants, table grain notes
│   ├── preprocessing/    # loading, cleaning, validation
│   ├── features/         # customer-level feature engineering (RFM etc.)
│   ├── segmentation/     # K-Means clustering + cluster profiling
│   ├── prediction/       # repeat-purchase classification model
│   ├── recommendation/   # popularity baseline + collaborative filtering
│   ├── nlp/               # review sentiment analysis (optional)
│   └── genai/             # LLM-powered explanations/summaries (optional)
├── models/               # serialized trained models (gitignored)
├── dashboard/            # Power BI .pbix + exported data
├── api/                  # FastAPI app
├── reports/              # final write-ups / figures
└── requirements.txt
```

## 6. Guidelines this project follows

- No merging tables before understanding their grain (see `src/config.py`).
- Time-aware train/test split for the prediction model (no leakage from future data).
- Baseline model (Logistic Regression) compared against a tree-based model (Random Forest).
- Evaluation beyond accuracy: Precision, Recall, F1, ROC-AUC, confusion matrix.
- Recommendation results reproducible from the stored pipeline/model.
