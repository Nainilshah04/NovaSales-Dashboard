"""
Page 3: Regional Analysis - Dynamic Theme
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from streamlit_app.utils.data_loader import load_data
from streamlit_app.utils.theme_manager import inject_theme_css, render_theme_toggle, lucide_icon
from streamlit_app.utils.chart_helpers import get_theme_colors, region_heatmap, product_region_bar

st.set_page_config(page_title="Regional Analysis", page_icon="🗺️", layout="wide")

# ── CSS & Theme ──────────────────────────────────────────────────
inject_theme_css()
c = get_theme_colors()

df = load_data()

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    render_theme_toggle()

# ── Header ────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg, var(--card-bg-solid), var(--bg-color));
            border: var(--card-border);
            padding:40px; border-radius:20px; margin-bottom:25px;
            box-shadow: var(--card-shadow);
            backdrop-filter: blur(12px);
            display: flex; align-items: center;">
    <div style="margin-right:20px;">
        {lucide_icon('globe', size=42, color='var(--accent-primary)')}
    </div>
    <div>
        <div style="color:var(--text-color); font-size:38px; font-weight:800;
                    letter-spacing:-0.02em; line-height:1.2;">
            Regional <span style="color:var(--accent-primary);">Analysis</span>
        </div>
        <div style="color:var(--muted-text); font-size:15px; margin-top:10px; font-weight:500;">
            Geographic performance across all NovaSales regions
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Region Stats Calculations ─────────────────────────────────────
rs = (df.groupby('region').agg(
    avg_att=('attainment_pct_display','mean'),
    total_pay=('total_payout','sum'),
    reps=('rep_id','nunique'),
    deals=('deals_closed','sum'),
    above=('attainment_pct', lambda x: (x>=1.0).sum()),
    total=('rep_id','count'),
).reset_index())
rs['hit_rate'] = (rs['above'] / rs['total'] * 100).round(1)

best = rs.loc[rs['avg_att'].idxmax()]
worst = rs.loc[rs['avg_att'].idxmin()]

# ── Best / Worst Cards ────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown(f"""
    <div class="custom-card" style="background:var(--success-bg) !important; border:2px solid var(--success) !important; text-align:center;">
        <div style="margin-bottom:8px; display:flex; justify-content:center;">
            {lucide_icon('trophy', size=36, color='var(--success)', extra_style='margin-right:0;')}
        </div>
        <div style="font-size:20px; font-weight:700; color:var(--success); margin:8px 0;">
            {best['region']} — Best Region
        </div>
        <div style="font-size:32px; font-weight:800; color:var(--text-color);">
            {best['avg_att']:.1f}% Attainment
        </div>
        <div style="color:var(--muted-text); font-size:13px; margin-top:8px;">
            <strong>{int(best['reps'])}</strong> reps • <strong>{best['hit_rate']:.0f}%</strong> quota hit •
            <strong>₹{best['total_pay']/10000000:.1f}Cr</strong> total payout
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="custom-card" style="background:var(--danger-bg) !important; border:2px solid var(--danger) !important; text-align:center;">
        <div style="margin-bottom:8px; display:flex; justify-content:center;">
            {lucide_icon('trending-down', size=36, color='var(--danger)', extra_style='margin-right:0;')}
        </div>
        <div style="font-size:20px; font-weight:700; color:var(--danger); margin:8px 0;">
            {worst['region']} — Needs Attention
        </div>
        <div style="font-size:32px; font-weight:800; color:var(--text-color);">
            {worst['avg_att']:.1f}% Attainment
        </div>
        <div style="color:var(--muted-text); font-size:13px; margin-top:8px;">
            <strong>{int(worst['reps'])}</strong> reps • <strong>{worst['hit_rate']:.0f}%</strong> quota hit •
            <strong>₹{worst['total_pay']/10000000:.1f}Cr</strong> total payout
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Region KPIs ───────────────────────────────────────────────────
st.markdown("### 📊 Regional Metrics")
rcols = st.columns(4)

for i, (_, row) in enumerate(rs.iterrows()):
    with rcols[i]:
        # Custom region card
        st.markdown(f"""
        <div class="custom-card" style="margin-bottom:0;">
            <div style="font-size:12px; color:var(--muted-text); font-weight:700; text-transform:uppercase; letter-spacing:0.08em; display:flex; align-items:center;">
                {lucide_icon('map-pin', size=14, color='var(--accent-primary)', extra_style='margin-right:4px;')}
                <span>{row['region']} Region</span>
            </div>
            <div style="font-size:30px; font-weight:800; color:var(--text-color); margin:5px 0;">
                {row['avg_att']:.1f}%
            </div>
            <div style="font-size:11px; color:var(--muted-text);">
                Total Payout: <strong>₹{row['total_pay']/100000:.1f}L</strong><br>
                Active Team: <strong>{int(row['reps'])} reps</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Heatmap ───────────────────────────────────────────────────────
st.markdown("### 🌡️ Region × Month Performance")
fig_h = region_heatmap(df)
st.plotly_chart(fig_h, use_container_width=True)

# ── Product Performance ───────────────────────────────────────────
st.markdown("### 📦 Product Line breakdowns")
p1, p2 = st.columns([3, 2])

with p1:
    fig_pb = product_region_bar(df)
    st.plotly_chart(fig_pb, use_container_width=True)

with p2:
    region_sel = st.selectbox("🗺️ Select Region for Revenue Mix", sorted(df['region'].unique()))
    prod_df = (df[df['region']==region_sel].groupby('product_line')
               .agg(total=('actual_sales','sum')).reset_index())
    
    # Custom colored pie chart matching themes
    fig_pie = go.Figure(go.Pie(
        labels=prod_df['product_line'], values=prod_df['total'],
        hole=0.5, marker=dict(colors=[c['primary'], c['success'], c['warning']]),
        textinfo='percent+label', textfont=dict(size=11, family='Manrope'),
    ))
    fig_pie.update_layout(
        title=f'<b>Revenue Product-Mix — {region_sel}</b>',
        title_font=dict(size=16, family='Manrope'),
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(color=c['text'], family='Manrope'),
        height=350,
        margin=dict(t=50, b=30, l=10, r=10),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Monthly Region Trend ──────────────────────────────────────────
st.markdown("### 📈 Monthly Trend by Region")
mr = (df.groupby(['region','month','month_label'])['attainment_pct_display']
      .mean().reset_index().sort_values('month'))

fig_mt = go.Figure()
for region in ['North','South','East','West']:
    rd = mr[mr['region'] == region]
    fig_mt.add_trace(go.Scatter(
        x=rd['month_label'], y=rd['attainment_pct_display'],
        name=region, mode='lines+markers',
        line=dict(color=c['regions'][region], width=2.5), 
        marker=dict(size=7),
    ))
    
fig_mt.add_hline(y=100, line_dash='dash', line_color=c['text'], annotation_text='Quota', annotation_font=dict(color=c['text']))

PLOTLY_THEME = dict(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color=c['text'], family='Manrope'),
    xaxis=dict(gridcolor=c['grid'], color=c['text']),
    yaxis=dict(gridcolor=c['grid'], color=c['text']),
)

fig_mt.update_layout(title='<b>Regional Trends — FY 2024</b>',
                      title_font=dict(size=16, family='Manrope'),
                      legend=dict(orientation='h', y=1.12),
                      hovermode='x unified', 
                      margin=dict(t=50, b=30, l=10, r=10),
                      **PLOTLY_THEME)
st.plotly_chart(fig_mt, use_container_width=True)