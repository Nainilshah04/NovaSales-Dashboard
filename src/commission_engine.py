"""
NovaSales Pvt Ltd - Commission Calculation Engine
Slab-based commission logic with accelerators and bonuses
"""

import pandas as pd
import numpy as np
import os

DEFAULT_SLABS = [
    {'min_pct': 0.00, 'max_pct': 0.50, 'rate': 0.00},
    {'min_pct': 0.50, 'max_pct': 0.80, 'rate': 0.05},
    {'min_pct': 0.80, 'max_pct': 1.00, 'rate': 0.10},
    {'min_pct': 1.00, 'max_pct': 1.20, 'rate': 0.15},
    {'min_pct': 1.20, 'max_pct': 9.99, 'rate': 0.20},
]
TOP_PERFORMER_BONUS_RATE = 0.05
TOP_PERFORMER_THRESHOLD = 0.90


def calculate_commission_rate(attainment_pct, slabs=None):
    if slabs is None:
        slabs = DEFAULT_SLABS
    rate = 0.0
    for slab in slabs:
        if slab['min_pct'] < attainment_pct <= slab['max_pct']:
            rate = slab['rate']
            break
        if attainment_pct == 0:
            rate = 0.0
            break
    return rate


def calculate_commission(actual_sales, monthly_target, slabs=None):
    if monthly_target <= 0:
        return {
            'attainment_pct': 0.0,
            'commission_rate': 0.0,
            'commission_earned': 0.0,
        }
    attainment_pct = actual_sales / monthly_target
    commission_rate = calculate_commission_rate(attainment_pct, slabs)
    commission_earned = actual_sales * commission_rate
    return {
        'attainment_pct': round(attainment_pct, 4),
        'commission_rate': commission_rate,
        'commission_earned': round(commission_earned, 2),
    }


def apply_top_performer_bonus(df, bonus_rate=TOP_PERFORMER_BONUS_RATE,
                                threshold=TOP_PERFORMER_THRESHOLD):
    df = df.copy()
    df['is_top_performer'] = False
    df['bonus_earned'] = 0.0

    for month in df['month'].unique():
        mask = df['month'] == month
        cutoff = df.loc[mask, 'attainment_pct'].quantile(threshold)
        top_mask = mask & (df['attainment_pct'] >= cutoff)
        df.loc[top_mask, 'is_top_performer'] = True
        df.loc[top_mask, 'bonus_earned'] = (
            df.loc[top_mask, 'actual_sales'] * bonus_rate
        ).round(2)
    return df


def calculate_total_payout(df):
    df = df.copy()
    df['monthly_base'] = (df['base_salary'] / 12).round(2)
    df['total_payout'] = (
        df['monthly_base'] + df['commission_earned'] + df['bonus_earned']
    ).round(2)
    df['total_compensation'] = df['total_payout']
    return df


def run_commission_engine(input_path='data/raw/sales_data.csv',
                           output_path='data/processed/commission_data.csv',
                           slabs=None):
    print("Loading raw sales data...")
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} rows")

    print("Calculating commissions...")
    commission_results = df.apply(
        lambda row: calculate_commission(
            row['actual_sales'], row['monthly_target'], slabs
        ),
        axis=1,
        result_type='expand'
    )
    df = pd.concat([df, commission_results], axis=1)

    print("Applying top performer bonuses...")
    df = apply_top_performer_bonus(df)

    print("Calculating total payouts...")
    df = calculate_total_payout(df)

    df['attainment_pct_display'] = (df['attainment_pct'] * 100).round(1)
    df['month_name'] = pd.to_datetime(
        df['year'].astype(str) + '-' + df['month'].astype(str) + '-01'
    ).dt.strftime('%b %Y')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"\nCommission Engine Complete")
    print(f"Total Rows: {len(df):,}")
    print(f"Total Commission: Rs.{df['commission_earned'].sum():,.0f}")
    print(f"Total Bonus: Rs.{df['bonus_earned'].sum():,.0f}")
    print(f"Total Payout: Rs.{df['total_payout'].sum():,.0f}")
    print(f"Avg Attainment: {df['attainment_pct_display'].mean():.1f}%")
    print(f"Saved to: {output_path}")
    return df


if __name__ == '__main__':
    df = run_commission_engine()
    print("\nSample Output:")
    cols = ['rep_id', 'name', 'month', 'actual_sales', 'monthly_target',
            'attainment_pct_display', 'commission_rate', 'commission_earned',
            'is_top_performer', 'bonus_earned', 'total_payout']
    print(df[cols].head(15).to_string(index=False))