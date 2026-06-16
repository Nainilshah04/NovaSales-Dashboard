"""
Page 1: Executive Overview - Dynamic Theme
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from streamlit_app.utils.data_loader import load_data, get_month_options
from streamlit_app.utils.theme_manager import inject_theme_css, render_theme_toggle, lucide_icon
from streamlit_app.utils.chart_helpers import get_theme_colors

st.set_page_config(page_title="Executive Overview", page_icon="🏠", layout="wide")

# ── CSS ──────────────────────────────────────────────────────────
inject_theme_css()

df = load_data()

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    render_theme_toggle()

# ── Header ───────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg, var(--card-bg-solid), var(--bg-color));
            border: var(--card-border);
            padding:40px; border-radius:20px; margin-bottom:30px;
            box-shadow: var(--card-shadow);
            backdrop-filter: blur(12px);
            display: flex; align-items: center;">
    <div style="margin-right:20px;">
        {lucide_icon('layout-dashboard', size=42, color='var(--accent-primary)')}
    </div>
    <div>
        <div style="color:var(--text-color); font-size:38px; font-weight:800;
                    letter-spacing:-0.02em; line-height:1.2;">
            Executive <span style="color:var(--accent-primary);">Overview</span>
        </div>
        <div style="color:var(--muted-text); font-size:15px; margin-top:10px; font-weight:500;">
            Real-time sales compensation insights for leadership
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Filters ──────────────────────────────────────────────────────
f1, f2, _ = st.columns([2, 2, 4])
with f1:
    month_options = get_month_options(df)
    selected_month = st.selectbox("📅 Month", month_options, index=len(month_options)-1)
with f2:
    region_opts = ['All Regions'] + sorted(df['region'].unique().tolist())
    selected_region = st.selectbox("🗺️ Region", region_opts)

month_df = df[df['month_label'] == selected_month]
if selected_region != 'All Regions':
    month_df = month_df[month_df['region'] == selected_region]

# ── KPI Calculations ─────────────────────────────────────────────
total_commission = month_df['commission_earned'].sum()
total_payout = month_df['total_payout'].sum()
total_reps = len(month_df)
reps_above = (month_df['attainment_pct'] >= 1.0).sum()
pct_above = (reps_above / total_reps * 100) if total_reps > 0 else 0
avg_attain = month_df['attainment_pct_display'].mean()
total_deals = month_df['deals_closed'].sum()

prev_month_num = month_df['month'].iloc[0] - 1 if len(month_df) > 0 else None
if prev_month_num and prev_month_num >= 1:
    prev_df = df[df['month'] == prev_month_num]
    if selected_region != 'All Regions':
        prev_df = prev_df[prev_df['region'] == selected_region]
    prev_pay = prev_df['total_payout'].sum()
    payout_chg = ((total_payout - prev_pay) / prev_pay * 100) if prev_pay > 0 else 0
else:
    payout_chg = 0

# Get current theme colors for local Plotly styling
c = get_theme_colors()

# ── KPI Cards ────────────────────────────────────────────────────
st.markdown("### 📊 Key Performance Indicators")

k1, k2, k3, k4, k5 = st.columns(5)

kpi_data = [
    (k1, "dollar-sign", "Total Payout", f"₹{total_payout/100000:.1f}L",
     f"{'▲' if payout_chg>=0 else '▼'} {abs(payout_chg):.1f}% MoM",
     c['success'] if payout_chg >= 0 else c['danger']),
    (k2, "award", "Quota Hit Rate", f"{pct_above:.0f}%",
     f"{reps_above}/{total_reps} reps", c['neutral']),
    (k3, "trending-up", "Avg Attainment", f"{avg_attain:.1f}%",
     "Team average", c['neutral']),
    (k4, "percent", "Commission Paid", f"₹{total_commission/100000:.1f}L",
     "Variable component", c['neutral']),
    (k5, "activity", "Deals Closed", f"{total_deals:,}",
     "This month", c['neutral']),
]

for col, icon_name, label, value, delta, delta_color in kpi_data:
    with col:
        st.markdown(f"""
        <div class="custom-card" style="padding:22px; margin-bottom:0;">
            <div style="margin-bottom:12px; height: 32px;">
                {lucide_icon(icon_name, size=28, color='var(--accent-primary)')}
            </div>
            <div style="font-size:11px; color:var(--muted-text); font-weight:600;
                        text-transform:uppercase; letter-spacing:0.08em;">{label}</div>
            <div style="font-size:30px; font-weight:800; color:var(--text-color);
                        margin:6px 0; letter-spacing:-0.02em;">{value}</div>
            <div style="font-size:12px; color:{delta_color}; font-weight:700;">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Top 5 Performers ─────────────────────────────────────────────
st.markdown("### 🌟 Top 5 Performers This Month")

top5 = month_df.nlargest(5, 'attainment_pct_display')
cols = st.columns(5)
medals = ['🥇', '🥈', '🥉', '🏅', '🏅']

for i, (_, row) in enumerate(top5.iterrows()):
    with cols[i]:
        st.markdown(f"""
        <div class="custom-card" style="text-align:center; padding:20px; margin-bottom:0; background:linear-gradient(135deg, var(--card-bg), var(--accent-light)) !important;">
            <div style="font-size:30px;">{medals[i]}</div>
            <div style="font-weight:700; color:var(--text-color); font-size:14px;
                        margin:10px 0 4px 0;">{row['name'].split()[0]}</div>
            <div style="color:var(--muted-text); font-size:11px;">
                {row['region']} • {row['product_line']}</div>
            <div style="color:var(--accent-primary); font-size:28px; font-weight:800;
                        margin:12px 0 4px 0;">{row['attainment_pct_display']:.0f}%</div>
            <div style="color:var(--success); font-size:12px; font-weight:700;">
                ₹{row['commission_earned']/1000:.0f}K earned</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ───────────────────────────────────────────────────────
st.markdown("### 📈 Trends & Distribution")

chart1, chart2 = st.columns([3, 2])

# Plotly theme configuration
PLOTLY_THEME = dict(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color=c['text'], family='Manrope'),
    xaxis=dict(gridcolor=c['grid'], color=c['text']),
    yaxis=dict(gridcolor=c['grid'], color=c['text']),
)

with chart1:
    trend_df = df.copy()
    if selected_region != 'All Regions':
        trend_df = trend_df[trend_df['region'] == selected_region]

    monthly = (trend_df.groupby(['month', 'month_label'], as_index=False)
                .agg(total_payout=('total_payout', 'sum'),
                     commission=('commission_earned', 'sum'))
                .sort_values('month'))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly['month_label'], y=monthly['total_payout'],
        name='Total Payout', mode='lines+markers',
        line=dict(color=c['primary'], width=4), marker=dict(size=10),
        fill='tozeroy', fillcolor=c['fill_primary'],
    ))
    fig.add_trace(go.Scatter(
        x=monthly['month_label'], y=monthly['commission'],
        name='Commission', mode='lines+markers',
        line=dict(color=c['success'], width=2.5, dash='dot'), marker=dict(size=7),
    ))
    fig.update_layout(
        title='<b>Monthly Payout Trend</b>',
        title_font=dict(size=16, family='Manrope'),
        xaxis_title='Month', yaxis_title='Amount (₹)',
        hovermode='x unified', legend=dict(orientation='h', y=1.12),
        margin=dict(t=50, b=30, l=10, r=10),
        **PLOTLY_THEME,
    )
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    bins = [0, 50, 80, 100, 120, 200]
    labels_b = ['0-50%', '51-80%', '81-100%', '101-120%', '120%+']
    month_df_c = month_df.copy()
    month_df_c['bucket'] = pd.cut(month_df_c['attainment_pct_display'],
                                   bins=bins, labels=labels_b)
    bc = month_df_c['bucket'].value_counts()

    # Dynamic colors for the pie slices matching themes
    pie_colors = [c['danger'], c['warning'], c['success'], c['primary'], c['accent_hover'] if st.session_state.theme == 'dark' else '#4C1D95']
    
    fig2 = go.Figure(go.Pie(
        labels=bc.index.tolist(), values=bc.values, hole=0.6,
        marker=dict(colors=pie_colors),
        textinfo='percent+label', textfont=dict(size=11, family='Manrope'),
    ))
    fig2.update_layout(
        title='<b>Attainment Distribution</b>',
        title_font=dict(size=16, family='Manrope'),
        paper_bgcolor='rgba(0,0,0,0)', font=dict(color=c['text'], family='Manrope'),
        height=400,
        margin=dict(t=50, b=30, l=10, r=10),
        annotations=[dict(text=f'<b>{total_reps}</b><br>REPS', x=0.5, y=0.5,
                          font_size=20, font_family='Manrope', showarrow=False,
                          font_color=c['text'])]
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Bottom: At-Risk + Region ─────────────────────────────────────
b1, b2 = st.columns(2)

with b1:
    st.markdown("### ⚠️ At-Risk Reps (< 60%)")
    at_risk = month_df[month_df['attainment_pct_display'] < 60].nsmallest(5, 'attainment_pct_display')
    if len(at_risk) == 0:
        st.success("✅ No at-risk reps this month!")
    else:
        for _, row in at_risk.iterrows():
            st.markdown(f"""
            <div style="background:var(--danger-bg); border:1px solid var(--danger);
                        border-radius:12px; padding:14px; margin:6px 0;
                        display:flex; justify-content:space-between; align-items:center;
                        box-shadow: var(--card-shadow);">
                <div style="display: flex; align-items: center;">
                    {lucide_icon('alert-triangle', size=16, color='var(--danger)', extra_style='margin-right:8px;')}
                    <div>
                        <strong style="color:var(--text-color);">{row['name']}</strong>
                        <span style="color:var(--muted-text); font-size:12px;"> • {row['region']}</span>
                    </div>
                </div>
                <span style="background:var(--danger); color:white; padding:4px 12px;
                             border-radius:20px; font-weight:700; font-size:13px;">
                    {row['attainment_pct_display']:.0f}%
                </span>
            </div>
            """, unsafe_allow_html=True)

with b2:
    st.markdown("### 🗺️ Region Performance")
    region_summary = (
        df[df['month_label'] == selected_month]
        .groupby('region').agg(avg_attain=('attainment_pct_display', 'mean'))
        .reset_index().sort_values('avg_attain', ascending=False)
    )
    fig3 = go.Figure(go.Bar(
        x=region_summary['region'], y=region_summary['avg_attain'],
        marker=dict(color=[c['primary'], c['success'], c['warning'], c['danger']]),
        text=region_summary['avg_attain'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
        textfont=dict(color=c['text'], family='Manrope'),
    ))
    fig3.add_hline(y=100, line_dash='dash', line_color=c['primary'],
                    annotation_text='Quota', annotation_font=dict(color=c['text']))
    fig3.update_layout(title='<b>Avg Attainment by Region</b>',
                        title_font=dict(size=16, family='Manrope'),
                        showlegend=False, height=350,
                        margin=dict(t=50, b=30, l=10, r=10),
                        **PLOTLY_THEME)
    st.plotly_chart(fig3, use_container_width=True)