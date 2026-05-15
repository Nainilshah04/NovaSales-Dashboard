# 💰 NovaSales Sales Compensation & Incentive Analytics Dashboard

## Business Problem
NovaSales Pvt Ltd (B2B SaaS) needed visibility into sales compensation:
who is earning what, who is hitting quota, and what happens if we change commission plans.

## Features
- 80 reps × 12 months = 960 rows synthetic data
- Slab-based commission engine (0%, 5%, 10%, 15%, 20%)
- 5-page Streamlit dashboard
- SQLite star schema database
- What-if incentive simulator
- Auto Excel report generator
- 18 Power BI DAX measures

## Quick Start
```bash
pip install -r requirements.txt
python setup.py
streamlit run streamlit_app/app.py

Tech Stack
Python | Pandas | NumPy | Faker | Plotly | Streamlit | SQLite | Power BI | DAX | Git