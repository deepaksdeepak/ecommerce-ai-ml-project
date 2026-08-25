import streamlit as st
import pandas as pd
import joblib
import pickle
import numpy as np

st.set_page_config(page_title="E-Commerce Customer Intelligence", layout="wide")

@st.cache_resource
def load_artifacts():
    kmeans_model = joblib.load('models/kmeans_model.pkl')
    rf_model = joblib.load('models/rf_model.pkl')
    customer_segments = pd.read_csv('models/customer_segments_full.csv')
    interactions_filtered = pd.read_csv('models/interactions_filtered.csv')
    product_popularity_df = pd.read_csv('models/product_popularity.csv')

    with open('models/item_similarity.pkl', 'rb') as f:
        item_similarity = pickle.load(f)
    with open('models/product_id_list.pkl', 'rb') as f:
        product_id_list = pickle.load(f)

    return kmeans_model, rf_model, customer_segments, interactions_filtered, product_popularity_df, item_similarity, product_id_list

kmeans_model, rf_model, customer_segments, interactions_filtered, product_popularity_df, item_similarity, product_id_list = load_artifacts()

customer_ids_cat = interactions_filtered['customer_unique_id'].astype('category')

def recommend_popular(n=5, exclude_products=None):
    recs = product_popularity_df['product_id'].tolist()
    if exclude_products:
        recs = [p for p in recs if p not in exclude_products]
    return recs[:n]

def recommend_for_customer(customer_id, n=5):
    if customer_id not in customer_ids_cat.cat.categories:
        already_bought = interactions_filtered[interactions_filtered['customer_unique_id'] == customer_id]['product_id'].tolist()
        return recommend_popular(n, exclude_products=already_bought)

    cust_rows = interactions_filtered[interactions_filtered['customer_unique_id'] == customer_id]
    purchased_products = cust_rows['product_id'].tolist()
    purchased_idx = [product_id_list.index(p) for p in purchased_products if p in product_id_list]

    if len(purchased_idx) == 0:
        return recommend_popular(n, exclude_products=purchased_products)

    scores = item_similarity[purchased_idx].sum(axis=0)
    for idx in purchased_idx:
        scores[idx] = -1

    top_idx = scores.argsort()[::-1][:n]
    return [product_id_list[i] for i in top_idx]

st.title("🛍️ E-Commerce Customer Intelligence & Recommendation System")
st.markdown("Enter a Customer ID to view their profile, segment, and personalized recommendations.")

customer_input = st.text_input("Customer Unique ID", placeholder="e.g. paste a customer_unique_id from the dataset")

sample_ids = customer_segments['customer_unique_id'].sample(5, random_state=1).tolist()
st.caption(f"Try one of these sample IDs: {', '.join(sample_ids)}")

if customer_input:
    customer_input_clean = customer_input.strip()
    customer_segments['customer_unique_id'] = customer_segments['customer_unique_id'].astype(str).str.strip()
    customer_row = customer_segments[customer_segments['customer_unique_id'] == customer_input_clean] 

    if customer_row.empty:
        st.error("Customer ID not found. Please check the ID and try again.")
    else:
        row = customer_row.iloc[0]

        col1, col2, col3 = st.columns(3)
        col1.metric("Segment", row['segment_name'])
        col2.metric("Recency (days)", f"{row['recency_days']:.0f}")
        col3.metric("Total Spend", f"R$ {row['monetary']:.2f}")

        col4, col5, col6 = st.columns(3)
        col4.metric("Frequency", f"{row['frequency']:.0f} orders")
        col5.metric("Avg Order Value", f"R$ {row['avg_order_value']:.2f}")
        col6.metric("Avg Review Score", f"{row['avg_review_score']:.1f} / 5")

        st.subheader("📦 Recommended Products")
        recs = recommend_for_customer(customer_input, n=5)
        rec_cols = st.columns(5)
        for i, prod_id in enumerate(recs):
            with rec_cols[i]:
                st.markdown(f"**#{i+1}**")
                st.code(prod_id, language=None)

        st.subheader("📊 Customer Profile Details")
        st.dataframe(customer_row.T, use_container_width=True)

st.markdown("---")
st.caption("E-Commerce Customer Intelligence Project — built on the Olist Brazilian E-Commerce dataset")