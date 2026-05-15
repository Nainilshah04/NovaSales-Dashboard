"""
Centralized data loading with caching for Streamlit app.
"""

import pandas as pd
import sqlite3
import streamlit as st
import os

DB_PATH = 'data/novasales.db'
CSV_PATH = 'data/processed/commission_data.csv'


@st.cache_data(ttl=3600)
def load_data():
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        query = """
            SELECT
                f.*,
                r.name,
                r.tenure_months,
                r.base_salary,
                d.quarter,
                d.month_name
            FROM fact_sales f
            JOIN dim_rep r ON f.rep_id = r.rep_id
            JOIN dim_date d ON f.date_id = d.date_id
        """
        df = pd.read_sql(query, conn)
        conn.close()
    else:
        df = pd.read_csv(CSV_PATH)

    df['attainment_pct_display'] = (df['attainment_pct'] * 100).round(1)
    df['month_label'] = pd.to_datetime(
        df['year'].astype(str) + '-' + df['month'].astype(str) + '-01'
    ).dt.strftime('%b %Y')
    return df


def get_month_options(df):
    months = df[['month', 'month_label']].drop_duplicates().sort_values('month')
    return months['month_label'].tolist()


def get_rep_options(df):
    return sorted(df['name'].unique().tolist())