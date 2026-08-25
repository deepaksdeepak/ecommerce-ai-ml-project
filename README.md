# E-Commerce Customer Intelligence & Recommendation System

An end-to-end AI/ML platform that analyzes customer behavior, segments customers, predicts repeat-purchase likelihood, and recommends products — built on the Olist Brazilian E-Commerce dataset.

## Business Problem

An e-commerce company wants to understand:
- Who are our customers and what are their purchasing patterns?
- Which customer segments are valuable, inactive, frequent, or price-sensitive?
- Which customers are likely to purchase again or show strong engagement?
- Which products should be recommended to a customer based on their previous behaviour?

## Dataset

**Primary dataset:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — ~100,000 orders from 2016–2018 across 9 relational CSV files (customers, orders, order items, products, payments, reviews, sellers, geolocation, category translations).

## Project Architecture

## Folder Structure

## Setup & Installation

1. **Clone the repository**
```bash
   git clone https://github.com/deepaksdeepak/ecommerce-ai-ml-project.git
   cd ecommerce-ai-ml-project
```

2. **Create and activate a virtual environment**
```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Download the dataset**
   - Download the [Olist dataset from Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
   - Extract all 9 CSVs into `data/raw/`

5. **Validate the data loads correctly**
```bash
   python -m src.preprocessing.load_data
```

6. **Run the notebook**
   Open `notebooks/01_data_understanding.ipynb` in VS Code / Jupyter and run all cells.

## Pipeline Summary

### Phase A — Data Understanding & Quality
- Validated the grain of every table (e.g., confirmed `order_items` is item-level, not order-level).
- Audited missing values and duplicates across all 9 tables.
- Investigated order status: **97.02% delivered**, with the remainder split across shipped, canceled, unavailable, invoiced, processing, created, and approved.
- Converted all date columns to proper datetime types.

### Phase B — Exploratory Data Analysis
- Revenue and order-volume trends over time.
- Customer distribution by state.
- Top/bottom product categories by revenue.
- Payment method behavior and installment patterns.
- Delivery performance and on-time delivery rate.
- Review score distribution.
- Customer purchase frequency and revenue concentration.

Key finding: **[FILL IN — e.g., "~97% of customers are one-time buyers; repeat purchase rate is only 0.87%"]**

### Phase C — Customer Feature Engineering
Built a customer-level analytical table (RFM + behavioral features) including:
- Recency, Frequency, Monetary (RFM)
- Average order value, items per order, freight cost
- Average review score
- Preferred payment type & product category
- Customer location
- Count of cancelled/unavailable orders

Saved to `data/processed/customer_features.csv`.

### Phase D — Customer Segmentation
K-Means clustering (K=4, selected via elbow method and silhouette score) on standardized, log-transformed RFM features.

| Segment | % of Customers | Description |
|---|---|---|
| High-Value One-Time Buyers | 40.6% | High spend (R$231 avg), high satisfaction, single purchase |
| Low-Value Budget Shoppers | 40.8% | Low spend (R$44 avg), satisfied, single purchase |
| Dissatisfied Customers | 15.6% | Moderate spend, low review scores (1.63 avg) — flagged for investigation |
| Loyal Repeat Customers | 3.0% | Only segment with real repeat behavior (2.11 orders avg), high spend, high satisfaction |

Saved to `data/processed/customer_segments.csv`.

### Phase E — Supervised ML: Repeat Purchase Prediction
- Time-aware train/test split using a purchase-date cutoff (no data leakage — features built only from pre-cutoff data).
- Target is heavily imbalanced: only **0.87%** of eligible customers made a repeat purchase.
- Models compared: Logistic Regression (baseline) vs Random Forest, both with `class_weight='balanced'`.

| Model | ROC-AUC | Recall (repeat class) | Precision (repeat class) |
|---|---|---|---|
| Logistic Regression | [FILL IN] | 0.58 | 0.01 |
| Random Forest | [FILL IN] | [FILL IN] | [FILL IN] |

**Business interpretation:** Given the rarity of repeat purchases, the model is best used to *rank* customers by likelihood score for targeted retention marketing, rather than as a hard yes/no classifier.

### Phase F — Product Recommendation System
- Popularity-based baseline (cold-start fallback).
- Item-based collaborative filtering using cosine similarity on a filtered customer-product interaction matrix.
- Already-purchased products excluded from recommendations.
- Evaluated via leave-one-out Hit Rate @ 5: **[FILL IN]**

Sample recommendations saved to `data/processed/sample_recommendations.csv`.

### SQL Analysis
8 business queries (revenue trends, category performance, delivery times by state, payment breakdowns, review-delay correlation, top sellers, revenue concentration) available in [`sql/business_queries.sql`](sql/business_queries.sql).

## Tech Stack

| Area | Tools |
|---|---|
| Data manipulation | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Recommendation | Scikit-learn (cosine similarity) |
| SQL | SQLite |
| Development | VS Code, Jupyter, Git/GitHub |

## Key Insights & Limitations

- The Olist dataset has an unusually low repeat-purchase rate, which limits classic RFM-style segmentation (recency/frequency show little variation) and makes supervised prediction a hard, imbalanced problem.
- Segments are primarily differentiated by **spend level** and **review score** rather than purchase frequency.
- The "Dissatisfied Customers" segment (15.6%, avg review 1.63) is a priority area for business investigation — likely tied to delivery delays or specific product categories.

## Dashboard

A Power BI dashboard (`dashboard/data/ecommerce_dashboard.pbix`) is included, covering:
- **Executive Overview**: Revenue trend, order volume, and average order value KPIs
- **Customer Analytics**: Segment distribution (donut + bar), RFM breakdown by segment (table), customer geography

All underlying data exports for further dashboard pages (Product Analytics, Operations, ML Insights, Recommendations) are prepared and available in `dashboard/data/`, ready for extension.

🔗 **[Live Demo](https://ecommerce-ai-ml-project-kqpcbgw3hpnp8ec4zdprfh.streamlit.app)** | 📊 [Power BI Dashboard](dashboard/data/ecommerce_dashboard.pbix)

## Author

Deepak — [GitHub](https://github.com/deepaksdeepak)
