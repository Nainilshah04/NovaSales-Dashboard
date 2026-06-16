"""
Page 2: Rep Performance - Dynamic Theme with Forma.ai "Go-Get" Cards
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from streamlit_app.utils.data_loader import load_data
from streamlit_app.utils.theme_manager import inject_theme_css, render_theme_toggle
from streamlit_app.utils.chart_helpers import (
    get_theme_colors, 
    attainment_gauge, 
    rep_quota_vs_actual_bar, 
    commission_line_chart
)

st.set_page_config(page_title="Rep Performance", page_icon="👤", layout="wide")

# ── CSS & Theme ──────────────────────────────────────────────────
inject_theme_css()
c = get_theme_colors()

df = load_data()

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    render_theme_toggle()

# ── Header ────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg, var(--card-bg-solid), var(--bg-color));
            border: var(--card-border);
            padding:40px; border-radius:20px; margin-bottom:25px;
            box-shadow: var(--card-shadow);
            backdrop-filter: blur(12px);">
    <div style="color:var(--text-color); font-size:38px; font-weight:800;
                letter-spacing:-0.02em; line-height:1.2;">
        👤 Rep Performance <span style="color:var(--accent-primary);">Drilldown</span>
    </div>
    <div style="color:var(--muted-text); font-size:15px; margin-top:10px; font-weight:500;">
        Deep-dive analytics for individual sales representatives
    </div>
</div>
""", unsafe_allow_html=True)

# ── Selector ──────────────────────────────────────────────────────
sel1, sel2 = st.columns([3, 5])
with sel1:
    selected_rep = st.selectbox("🔍 Select Rep", sorted(df['name'].unique().tolist()))

rep_df = df[df['name'] == selected_rep].sort_values('month')
info = rep_df.iloc[0]
avg_attain = rep_df['attainment_pct_display'].mean()
total_earnings = rep_df['commission_earned'].sum() + rep_df['bonus_earned'].sum()
best_month = rep_df.loc[rep_df['attainment_pct_display'].idxmax(), 'month_label']
top_months = rep_df['is_top_performer'].sum()

# ── Rep Profile Card ──────────────────────────────────────────────
st.markdown(f"""
<div class="custom-card" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">
    <div>
        <div style="font-size:26px; font-weight:800; color:var(--text-color);">
            👤 {selected_rep}
        </div>
        <div style="margin-top:10px; display:flex; gap:8px; flex-wrap:wrap;">
            <span style="background:var(--accent-light); border:var(--card-border);
                        padding:5px 14px; border-radius:20px;
                        font-size:12px; color:var(--text-color); font-weight:600;">🗺️ {info['region']}</span>
            <span style="background:var(--accent-light); border:var(--card-border);
                        padding:5px 14px; border-radius:20px;
                        font-size:12px; color:var(--text-color); font-weight:600;">📦 {info['product_line']}</span>
            <span style="background:var(--accent-light); border:var(--card-border);
                        padding:5px 14px; border-radius:20px;
                        font-size:12px; color:var(--text-color); font-weight:600;">⏱️ {int(info['tenure_months'])} months tenure</span>
            <span style="background:var(--accent-light); border:var(--card-border);
                        padding:5px 14px; border-radius:20px;
                        font-size:12px; color:var(--text-color); font-weight:600;">💼 ₹{info['base_salary']/100000:.1f}L base salary</span>
        </div>
    </div>
    <div style="text-align:right;">
        <div style="font-size:42px; color:var(--accent-primary); font-weight:800; line-height:1;">{avg_attain:.1f}%</div>
        <div style="color:var(--muted-text); font-size:13px; font-weight:600;">Avg Attainment</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("💰 Variable Earnings", f"₹{total_earnings/1000:.1f}K")
with k2:
    st.metric("📊 Total Sales", f"₹{rep_df['actual_sales'].sum()/100000:.1f}L")
with k3:
    st.metric("🤝 Total Deals", f"{rep_df['deals_closed'].sum()}")
with k4:
    st.metric("⭐ Best Month", best_month)

st.markdown("<br>", unsafe_allow_html=True)

# ── Forma.ai "Go-Get" Motivational Card ───────────────────────────
latest_row = rep_df.iloc[-1]
target = latest_row['monthly_target']
actual = latest_row['actual_sales']
attainment = latest_row['attainment_pct_display']
commission = latest_row['commission_earned']

if attainment < 100:
    deficit = target - actual
    est_bump = (target * 0.10) - commission
    est_bump = max(est_bump, 0.0)
    goget_html = f"""
    <div style="background: linear-gradient(135deg, var(--card-bg-solid), var(--accent-light)); 
                border: 1px solid var(--accent-primary); border-radius: 16px; padding: 24px; margin-bottom: 25px;
                box-shadow: var(--card-shadow); backdrop-filter: blur(12px);">
        <div style="font-size: 12px; font-weight: 700; color: var(--accent-primary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">
            🚀 Forma.ai Motivational Insight
        </div>
        <div style="font-size: 20px; font-weight: 800; color: var(--text-color); line-height: 1.3;">
            Close <span style="color: var(--accent-primary);">₹{deficit:,.0f}</span> more in sales to hit <strong>100% Quota</strong>!
        </div>
        <div style="font-size: 14px; color: var(--muted-text); margin-top: 10px;">
            Hitting this goal will unlock the <strong>10% Commission Slab</strong>, boosting your estimated payout by <strong style="color: var(--success);">+₹{est_bump:,.0f}</strong>.
        </div>
    </div>
    """
elif attainment < 120:
    deficit = (target * 1.20) - actual
    est_bump = ((target * 1.2) * 0.20) - commission
    est_bump = max(est_bump, 0.0)
    goget_html = f"""
    <div style="background: linear-gradient(135deg, var(--card-bg-solid), var(--accent-light)); 
                border: 1px solid var(--accent-primary); border-radius: 16px; padding: 24px; margin-bottom: 25px;
                box-shadow: var(--card-shadow); backdrop-filter: blur(12px);">
        <div style="font-size: 12px; font-weight: 700; color: var(--accent-primary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">
            🚀 Forma.ai Accelerator Target
        </div>
        <div style="font-size: 20px; font-weight: 800; color: var(--text-color); line-height: 1.3;">
            Close <span style="color: var(--accent-primary);">₹{deficit:,.0f}</span> more in sales to unlock the <strong>120%+ Accelerator Tier</strong>!
        </div>
        <div style="font-size: 14px; color: var(--muted-text); margin-top: 10px;">
            Crossing this threshold increases your commission rate to <strong>20% (Double Slab)</strong>, adding approximately <strong style="color: var(--success);">+₹{est_bump:,.0f}</strong> to your variable earnings.
        </div>
    </div>
    """
else:
    goget_html = f"""
    <div style="background: linear-gradient(135deg, var(--card-bg-solid), var(--success-bg)); 
                border: 1px solid var(--success); border-radius: 16px; padding: 24px; margin-bottom: 25px;
                box-shadow: var(--card-shadow); backdrop-filter: blur(12px);">
        <div style="font-size: 12px; font-weight: 700; color: var(--success); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">
            🏆 Outstanding Performance
        </div>
        <div style="font-size: 20px; font-weight: 800; color: var(--text-color); line-height: 1.3;">
            Currently in the **Top Accelerator Slab** ({attainment:.1f}% Attainment)!
        </div>
        <div style="font-size: 14px; color: var(--muted-text); margin-top: 10px;">
            You have earned <strong style="color: var(--success);">₹{commission:,.0f}</strong> in commissions this month. Keep driving sales to maximize your uncapped payouts!
        </div>
    </div>
    """
st.markdown(goget_html, unsafe_allow_html=True)

# ── Gauge + Table ─────────────────────────────────────────────────
g_col, t_col = st.columns([1, 2])

with g_col:
    # Use reusable attainment_gauge from chart_helpers
    fig_g = attainment_gauge(latest_row['attainment_pct_display'], selected_rep)
    st.plotly_chart(fig_g, use_container_width=True)

with t_col:
    st.markdown("**📅 Monthly Performance Details**")
    show_df = rep_df[['month_label','monthly_target','actual_sales',
                       'attainment_pct_display','commission_earned',
                       'bonus_earned','deals_closed']].copy()
    show_df.columns = ['Month','Target','Actual','Attainment %',
                        'Commission','Bonus','Deals']
    
    # Check theme to apply a clean styled table
    st.dataframe(
        show_df.style
        .background_gradient(subset=['Attainment %'], cmap='Purples' if st.session_state.theme == 'dark' else 'RdYlGn', vmin=50, vmax=130)
        .format({'Target':'₹{:,.0f}','Actual':'₹{:,.0f}',
                 'Attainment %':'{:.1f}%','Commission':'₹{:,.0f}','Bonus':'₹{:,.0f}'}),
        use_container_width=True, height=280,
    )

# ── Charts Row ────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    fig_bar = rep_quota_vs_actual_bar(rep_df)
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    fig_line = commission_line_chart(rep_df)
    st.plotly_chart(fig_line, use_container_width=True)

# ── Attainment Trend ──────────────────────────────────────────────
rep_sorted = rep_df.sort_values('month')
fig_at = go.Figure()
fig_at.add_trace(go.Scatter(
    x=rep_sorted['month_label'], y=rep_sorted['attainment_pct_display'],
    mode='lines+markers+text', line=dict(color=c['primary'], width=3),
    marker=dict(size=10, color=rep_sorted['attainment_pct_display'].apply(
        lambda x: c['success'] if x >= 100 else c['danger'])),
    text=rep_sorted['attainment_pct_display'].apply(lambda x: f'{x:.0f}%'),
    textposition='top center', textfont=dict(size=10, color=c['text'], family='Manrope'),
))
fig_at.add_hline(y=100, line_dash='dash', line_color=c['success'], annotation_text='Quota', annotation_font=dict(color=c['success']))
fig_at.add_hline(y=80, line_dash='dot', line_color=c['warning'], annotation_text='Warning', annotation_font=dict(color=c['warning']))
fig_at.update_layout(title=f'<b>{selected_rep} — Attainment Trend Over Time</b>',
                      title_font=dict(size=16, family='Manrope'),
                      yaxis_range=[0, max(rep_sorted['attainment_pct_display'].max()+20, 140)],
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                      font=dict(color=c['text'], family='Manrope'),
                      xaxis=dict(color=c['text']),
                      yaxis=dict(color=c['text'], gridcolor=c['grid']),
                      margin=dict(t=50, b=30, l=10, r=10))
st.plotly_chart(fig_at, use_container_width=True)

# ── Peer Comparison ───────────────────────────────────────────────
st.markdown("### 🔄 Peer Comparison")
peers = (
    df[(df['region']==info['region']) & (df['product_line']==info['product_line'])]
    .groupby('name').agg(avg_att=('attainment_pct_display','mean'))
    .reset_index().sort_values('avg_att', ascending=False)
)
peers['highlight'] = peers['name'] == selected_rep

fig_p = px.bar(peers, x='name', y='avg_att', color='highlight',
               color_discrete_map={True: c['primary'], False: c['fill_primary']},
               title=f'<b>Peer Comparison — {info["region"]} | {info["product_line"]}</b>')
fig_p.add_hline(y=100, line_dash='dash', line_color=c['text'])
fig_p.update_layout(
    showlegend=False, 
    xaxis_tickangle=-45,
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color=c['text'], family='Manrope'),
    xaxis=dict(color=c['text']),
    yaxis=dict(color=c['text'], gridcolor=c['grid']),
    margin=dict(t=50, b=30, l=10, r=10)
)
st.plotly_chart(fig_p, use_container_width=True)