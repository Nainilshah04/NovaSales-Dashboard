"""
Page 1: Executive Overview - Forma.ai Purple Theme
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from streamlit_app.utils.data_loader import load_data, get_month_options

st.set_page_config(page_title="Executive Overview", page_icon="🏠", layout="wide")

# ── CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Manrope', sans-serif !important; }
.stApp { background: #FFFFFF; color: #1A0B2E; }
[data-testid="stSidebar"] { background: #FAFAFC; border-right: 1px solid #E9E5F5; }
h1,h2,h3 { font-family:'Manrope',sans-serif !important; font-weight:800 !important; color:#1A0B2E !important; }
#MainMenu, footer, header { visibility: hidden; }
.stSelectbox > div > div { background:#F5F3FF !important; border:1px solid #E9E5F5 !important; border-radius:10px !important; }
[data-testid="stMetric"] { background:#F5F3FF; border:1px solid #E9E5F5; border-radius:14px; padding:20px; }
</style>
""", unsafe_allow_html=True)

df = load_data()

# ── Header ───────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#1A0B2E,#2D1B4E);
            padding:40px; border-radius:20px; margin-bottom:30px;
            box-shadow: 0 10px 40px rgba(109,40,217,0.15);">
    <div style="color:#FFFFFF; font-size:38px; font-weight:800;
                letter-spacing:-0.02em; line-height:1.2;">
        🏠 Executive <span style="color:#A78BFA;">Overview</span>
    </div>
    <div style="color:#C4B5FD; font-size:15px; margin-top:10px; font-weight:500;">
        Real-time sales compensation insights for leadership
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

# ── KPI Cards ────────────────────────────────────────────────────
st.markdown("### 📊 Key Performance Indicators")

k1, k2, k3, k4, k5 = st.columns(5)

kpi_data = [
    (k1, "💰", "Total Payout", f"₹{total_payout/100000:.1f}L",
     f"{'▲' if payout_chg>=0 else '▼'} {abs(payout_chg):.1f}% MoM",
     "#10B981" if payout_chg >= 0 else "#EF4444"),
    (k2, "🏆", "Quota Hit Rate", f"{pct_above:.0f}%",
     f"{reps_above}/{total_reps} reps", "#64748B"),
    (k3, "📈", "Avg Attainment", f"{avg_attain:.1f}%",
     "Team average", "#64748B"),
    (k4, "🎯", "Commission Paid", f"₹{total_commission/100000:.1f}L",
     "Variable component", "#64748B"),
    (k5, "🤝", "Deals Closed", f"{total_deals:,}",
     "This month", "#64748B"),
]

for col, icon, label, value, delta, delta_color in kpi_data:
    with col:
        st.markdown(f"""
        <div style="background:white; border:1px solid #E9E5F5;
                    border-radius:16px; padding:22px;">
            <div style="font-size:28px; margin-bottom:12px;">{icon}</div>
            <div style="font-size:11px; color:#64748B; font-weight:600;
                        text-transform:uppercase; letter-spacing:0.08em;">{label}</div>
            <div style="font-size:30px; font-weight:800; color:#1A0B2E;
                        margin:6px 0; letter-spacing:-0.02em;">{value}</div>
            <div style="font-size:12px; color:{delta_color}; font-weight:600;">{delta}</div>
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
        <div style="background:linear-gradient(135deg,#F5F3FF,#EDE9FE);
                    border:1px solid #DDD6FE; border-radius:16px;
                    padding:20px; text-align:center;">
            <div style="font-size:30px;">{medals[i]}</div>
            <div style="font-weight:700; color:#1A0B2E; font-size:14px;
                        margin:10px 0 4px 0;">{row['name'].split()[0]}</div>
            <div style="color:#64748B; font-size:11px;">
                {row['region']} • {row['product_line']}</div>
            <div style="color:#6D28D9; font-size:28px; font-weight:800;
                        margin:12px 0 4px 0;">{row['attainment_pct_display']:.0f}%</div>
            <div style="color:#10B981; font-size:12px; font-weight:600;">
                ₹{row['commission_earned']/1000:.0f}K earned</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ───────────────────────────────────────────────────────
st.markdown("### 📈 Trends & Distribution")

chart1, chart2 = st.columns([3, 2])

PURPLE_THEME = dict(
    plot_bgcolor='white', paper_bgcolor='white',
    font=dict(color='#1A0B2E', family='Manrope'),
    xaxis=dict(gridcolor='#F5F3FF'),
    yaxis=dict(gridcolor='#F5F3FF'),
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
        line=dict(color='#6D28D9', width=4), marker=dict(size=10),
        fill='tozeroy', fillcolor='rgba(109,40,217,0.08)',
    ))
    fig.add_trace(go.Scatter(
        x=monthly['month_label'], y=monthly['commission'],
        name='Commission', mode='lines+markers',
        line=dict(color='#A78BFA', width=2.5, dash='dot'), marker=dict(size=7),
    ))
    fig.update_layout(
        title='<b>Monthly Payout Trend</b>',
        xaxis_title='Month', yaxis_title='Amount (₹)',
        hovermode='x unified', legend=dict(orientation='h', y=1.12),
        **PURPLE_THEME,
    )
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    bins = [0, 50, 80, 100, 120, 200]
    labels_b = ['0-50%', '51-80%', '81-100%', '101-120%', '120%+']
    month_df_c = month_df.copy()
    month_df_c['bucket'] = pd.cut(month_df_c['attainment_pct_display'],
                                   bins=bins, labels=labels_b)
    bc = month_df_c['bucket'].value_counts()

    fig2 = go.Figure(go.Pie(
        labels=bc.index.tolist(), values=bc.values, hole=0.6,
        marker=dict(colors=['#FCA5A5','#FCD34D','#86EFAC','#A78BFA','#6D28D9']),
        textinfo='percent+label', textfont=dict(size=11),
    ))
    fig2.update_layout(
        title='<b>Attainment Distribution</b>',
        paper_bgcolor='white', font=dict(color='#1A0B2E', family='Manrope'),
        height=400,
        annotations=[dict(text=f'<b>{total_reps}</b><br>REPS', x=0.5, y=0.5,
                          font_size=20, showarrow=False)]
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
            <div style="background:#FEF2F2; border:1px solid #FEE2E2;
                        border-radius:12px; padding:14px; margin:6px 0;
                        display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <strong style="color:#1A0B2E;">⚠️ {row['name']}</strong>
                    <span style="color:#64748B; font-size:12px;"> • {row['region']}</span>
                </div>
                <span style="background:#EF4444; color:white; padding:4px 12px;
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
        marker=dict(color=['#6D28D9','#8B5CF6','#A78BFA','#C4B5FD']),
        text=region_summary['avg_attain'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
    ))
    fig3.add_hline(y=100, line_dash='dash', line_color='#6D28D9',
                    annotation_text='Quota')
    fig3.update_layout(title='<b>Avg Attainment by Region</b>',
                        showlegend=False, height=350, **PURPLE_THEME)
    st.plotly_chart(fig3, use_container_width=True)