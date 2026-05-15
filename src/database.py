"""
NovaSales Pvt Ltd - SQLite Database Builder
Star schema with fact + dimension tables
"""

import sqlite3
import pandas as pd
import os

DB_PATH = 'data/novasales.db'


def get_connection():
    os.makedirs('data', exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_schema(conn):
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS dim_rep (
            rep_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            region TEXT NOT NULL,
            product_line TEXT NOT NULL,
            tenure_months INTEGER,
            base_salary REAL
        );

        CREATE TABLE IF NOT EXISTS dim_region (
            region_id TEXT PRIMARY KEY,
            region_name TEXT NOT NULL,
            hq_city TEXT
        );

        CREATE TABLE IF NOT EXISTS dim_product (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT
        );

        CREATE TABLE IF NOT EXISTS dim_date (
            date_id TEXT PRIMARY KEY,
            month INTEGER,
            year INTEGER,
            quarter TEXT,
            month_name TEXT,
            is_q4 INTEGER
        );

        CREATE TABLE IF NOT EXISTS fact_sales (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rep_id TEXT,
            region TEXT,
            product_line TEXT,
            date_id TEXT,
            month INTEGER,
            year INTEGER,
            monthly_target REAL,
            actual_sales REAL,
            deals_closed INTEGER,
            attainment_pct REAL,
            commission_rate REAL,
            commission_earned REAL,
            bonus_earned REAL,
            monthly_base REAL,
            total_payout REAL,
            is_top_performer INTEGER,
            FOREIGN KEY (rep_id) REFERENCES dim_rep(rep_id),
            FOREIGN KEY (region) REFERENCES dim_region(region_id),
            FOREIGN KEY (product_line) REFERENCES dim_product(product_id),
            FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
        );
    """)
    conn.commit()
    print("Schema created")


def load_dimensions(conn, df):
    cursor = conn.cursor()

    rep_df = df[['rep_id', 'name', 'region', 'product_line',
                  'tenure_months', 'base_salary']].drop_duplicates('rep_id')
    rep_df.to_sql('dim_rep', conn, if_exists='replace', index=False)
    print(f"dim_rep loaded: {len(rep_df)} rows")

    region_meta = {
        'North': 'New Delhi', 'South': 'Bengaluru',
        'East': 'Kolkata', 'West': 'Mumbai',
    }
    region_data = [(r, r, region_meta[r]) for r in REGIONS]
    cursor.executemany(
        "INSERT OR REPLACE INTO dim_region VALUES (?,?,?)", region_data
    )

    product_data = [
        ('CloudCore', 'CloudCore', 'Cloud Infrastructure'),
        ('DataSync', 'DataSync', 'Data Integration'),
        ('SecureAPI', 'SecureAPI', 'API Security'),
    ]
    cursor.executemany(
        "INSERT OR REPLACE INTO dim_product VALUES (?,?,?)", product_data
    )

    quarter_map = {1:'Q1',2:'Q1',3:'Q1',4:'Q2',5:'Q2',6:'Q2',
                   7:'Q3',8:'Q3',9:'Q3',10:'Q4',11:'Q4',12:'Q4'}
    month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                   7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    date_data = []
    for m in range(1, 13):
        date_id = f"2024-{str(m).zfill(2)}"
        quarter = quarter_map[m]
        is_q4 = 1 if quarter == 'Q4' else 0
        date_data.append((date_id, m, 2024, quarter, month_names[m], is_q4))
    cursor.executemany(
        "INSERT OR REPLACE INTO dim_date VALUES (?,?,?,?,?,?)", date_data
    )
    conn.commit()
    print("Dimensions loaded")


REGIONS = ['North', 'South', 'East', 'West']


def load_fact_table(conn, df):
    fact_df = df.copy()
    fact_df['date_id'] = '2024-' + fact_df['month'].astype(str).str.zfill(2)
    fact_df['is_top_performer'] = fact_df['is_top_performer'].astype(int)
    cols = ['rep_id', 'region', 'product_line', 'date_id', 'month', 'year',
            'monthly_target', 'actual_sales', 'deals_closed', 'attainment_pct',
            'commission_rate', 'commission_earned', 'bonus_earned',
            'monthly_base', 'total_payout', 'is_top_performer']
    fact_df[cols].to_sql('fact_sales', conn, if_exists='replace', index=False)
    print(f"fact_sales loaded: {len(fact_df)} rows")


def build_database(commission_data_path='data/processed/commission_data.csv'):
    print("Building SQLite database...")
    df = pd.read_csv(commission_data_path)
    conn = get_connection()
    create_schema(conn)
    load_dimensions(conn, df)
    load_fact_table(conn, df)

    cursor = conn.cursor()
    for table in ['dim_rep', 'dim_region', 'dim_product', 'dim_date', 'fact_sales']:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")

    conn.close()
    print(f"\nDatabase saved to: {DB_PATH}")


if __name__ == '__main__':
    build_database()