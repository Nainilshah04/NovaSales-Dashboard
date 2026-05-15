"""
NovaSales Pvt Ltd - Synthetic Data Generator
Generates 960 rows (80 reps x 12 months) of realistic sales data
"""

import pandas as pd
import numpy as np
from faker import Faker
import os
import random

np.random.seed(42)
random.seed(42)
fake = Faker('en_IN')
Faker.seed(42)

REGIONS = ['North', 'South', 'East', 'West']
PRODUCT_LINES = ['CloudCore', 'DataSync', 'SecureAPI']
N_REPS = 80
MONTHS = list(range(1, 13))
YEAR = 2024

ARCHETYPES = {
    'star': {'weight': 0.20, 'mean_attain': 1.18, 'std': 0.08},
    'solid': {'weight': 0.50, 'mean_attain': 0.95, 'std': 0.12},
    'struggler': {'weight': 0.30, 'mean_attain': 0.65, 'std': 0.15},
}

SEASONALITY = {
    1: 0.78, 2: 0.80, 3: 1.05,
    4: 0.88, 5: 0.92, 6: 1.10,
    7: 0.82, 8: 0.85, 9: 1.08,
    10: 1.12, 11: 1.18, 12: 1.35,
}

REGION_SALARY = {
    'North': (800000, 1400000),
    'South': (750000, 1300000),
    'East': (700000, 1200000),
    'West': (850000, 1500000),
}

PRODUCT_TARGETS = {
    'CloudCore': (400000, 700000),
    'DataSync': (300000, 550000),
    'SecureAPI': (350000, 600000),
}


def assign_archetype():
    archetypes = list(ARCHETYPES.keys())
    weights = [ARCHETYPES[a]['weight'] for a in archetypes]
    return random.choices(archetypes, weights=weights, k=1)[0]


def generate_rep_master():
    reps = []
    used_names = set()
    region_pool = (REGIONS * (N_REPS // len(REGIONS) + 1))[:N_REPS]
    random.shuffle(region_pool)
    product_pool = (PRODUCT_LINES * (N_REPS // len(PRODUCT_LINES) + 1))[:N_REPS]
    random.shuffle(product_pool)

    for i in range(N_REPS):
        while True:
            name = fake.name()
            if name not in used_names:
                used_names.add(name)
                break

        region = region_pool[i]
        product_line = product_pool[i]
        archetype = assign_archetype()
        salary_range = REGION_SALARY[region]
        base_salary = random.randint(*salary_range)
        tenure = random.randint(3, 72)
        target_range = PRODUCT_TARGETS[product_line]
        monthly_target = random.randint(*target_range)

        reps.append({
            'rep_id': f'REP{str(i + 1).zfill(3)}',
            'name': name,
            'region': region,
            'product_line': product_line,
            'tenure_months': tenure,
            'base_salary': base_salary,
            'monthly_target': monthly_target,
            'archetype': archetype,
        })

    return pd.DataFrame(reps)


def generate_monthly_performance(rep, month):
    arch = ARCHETYPES[rep['archetype']]
    season = SEASONALITY[month]
    attainment = np.random.normal(arch['mean_attain'], arch['std'])
    attainment = max(0.10, attainment)
    attainment_seasonal = attainment * season
    actual_sales = rep['monthly_target'] * attainment_seasonal
    actual_sales = max(0, round(actual_sales, -2))
    base_deals = max(2, int(attainment_seasonal * 8))
    deals_closed = max(1, base_deals + random.randint(-2, 2))

    return {
        'actual_sales': actual_sales,
        'deals_closed': deals_closed,
    }


def build_dataset():
    rep_master = generate_rep_master()
    rows = []

    for month in MONTHS:
        for _, rep in rep_master.iterrows():
            perf = generate_monthly_performance(rep.to_dict(), month)
            rows.append({
                'rep_id': rep['rep_id'],
                'name': rep['name'],
                'region': rep['region'],
                'product_line': rep['product_line'],
                'tenure_months': rep['tenure_months'],
                'base_salary': rep['base_salary'],
                'monthly_target': rep['monthly_target'],
                'actual_sales': perf['actual_sales'],
                'deals_closed': perf['deals_closed'],
                'month': month,
                'year': YEAR,
            })

    df = pd.DataFrame(rows)
    df = df.sort_values(['month', 'rep_id']).reset_index(drop=True)
    print(f"Dataset generated: {len(df)} rows, {df['rep_id'].nunique()} reps")
    return df


if __name__ == '__main__':
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    df = build_dataset()
    output_path = 'data/raw/sales_data.csv'
    df.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")
    print(df.head(10).to_string())